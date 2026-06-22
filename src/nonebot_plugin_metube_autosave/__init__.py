import asyncio
import re
from urllib.parse import urlparse

from nonebot import logger, on_message
from nonebot.adapters import Bot, Event
from nonebot.exception import FinishedException
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .client import MeTubeClient
from .config import Config, plugin_config
from .model import AddTaskPayload

__plugin_meta__ = PluginMetadata(
    name="MeTube AutoSave",
    description="Minimal MeTube plugin: 1 -> link+mode -> auto download",
    usage="发送 1 后按提示发送：视频链接 空格 1/2",
    type="application",
    homepage="https://github.com/lzylipu/metube-autosave-bot",
    config=Config,
    supported_adapters=inherit_supported_adapters(),
    extra={"author": "lzylipu"},
)

# 等待状态 + 60秒自动超时清理
WAITING_USERS: dict[str, float] = {}  # user_key -> timestamp
PROGRESS_TASKS: dict[str, asyncio.Task] = {}
WAIT_TIMEOUT = 60.0

metube_handler = on_message(permission=SUPERUSER, block=True)

SUPPORTED_SCHEMES = {"http", "https"}
YOUTUBE_HOSTS = {
    "youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "music.youtube.com",
}
BILIBILI_HOSTS = {
    "bilibili.com", "www.bilibili.com", "m.bilibili.com", "b23.tv",
}
INVALID_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".txt"}


class RequestParseError(ValueError):
    pass


def _cleanup_expired_users():
    """清理超时的等待状态"""
    try:
        loop = asyncio.get_running_loop()
        now = loop.time()
    except RuntimeError:
        return
    expired = [k for k, t in WAITING_USERS.items() if now - t > WAIT_TIMEOUT]
    for k in expired:
        del WAITING_USERS[k]


def get_user_key(event: Event) -> str:
    try:
        return str(event.get_user_id())
    except Exception:
        return "unknown"


def get_text(event: Event) -> str:
    try:
        return str(event.get_plaintext()).strip()
    except Exception:
        return str(getattr(event, "message", "")).strip()


def detect_source(host: str) -> str:
    host = host.lower().strip()
    if host in YOUTUBE_HOSTS:
        return "YouTube"
    if host in BILIBILI_HOSTS:
        return "B站"
    return "Other"


def normalize_url(text: str) -> tuple[str, str]:
    raw = text.strip()
    if not raw or any(ch in raw for ch in ["\n", "\r", "\t"]):
        raise RequestParseError("invalid url")

    parsed = urlparse(raw)
    if parsed.scheme not in SUPPORTED_SCHEMES:
        raise RequestParseError("invalid scheme")
    if not parsed.netloc:
        raise RequestParseError("missing host")
    if parsed.username or parsed.password:
        raise RequestParseError("auth in url not allowed")

    host = parsed.netloc.lower().split(":")[0]
    if host in {"localhost", "127.0.0.1", "0.0.0.0"}:
        raise RequestParseError("localhost not allowed")
    if "." not in host:
        raise RequestParseError("invalid host")

    path_lower = (parsed.path or "").lower()
    if any(path_lower.endswith(ext) for ext in INVALID_SUFFIXES):
        raise RequestParseError("unsupported resource")
    if not parsed.path and not parsed.query:
        raise RequestParseError("too generic")

    return raw, detect_source(host)


def parse_request(text: str) -> tuple[AddTaskPayload, str, str]:
    parts = text.strip().rsplit(maxsplit=1)
    if len(parts) != 2:
        raise RequestParseError("missing mode (usage: link 1=video, link 2=mp3)")
    url_part, mode = parts
    url, source = normalize_url(url_part)

    if mode == "1":
        payload = AddTaskPayload(url=url, quality="best", format="any", auto_start=True)
        mode_hint = "视频"
    elif mode == "2":
        payload = AddTaskPayload(url=url, quality="best", format="mp3", auto_start=True)
        mode_hint = "音频"
    else:
        raise RequestParseError("invalid mode (1=video, 2=mp3)")

    return payload, source, mode_hint


async def monitor_progress(bot: Bot, event: Event, url: str, source: str, mode_hint: str):
    """后台监控下载进度，推送通知"""
    last_progress = None
    try:
        loop = asyncio.get_running_loop()
        deadline = loop.time() + plugin_config.progress_timeout_seconds
        while loop.time() < deadline:
            await asyncio.sleep(plugin_config.progress_interval_seconds)
            try:
                async with MeTubeClient() as client:
                    history = await client.get_history()
            except Exception as e:
                logger.warning(f"Progress poll failed: {e}")
                continue

            found = history.find_by_url(url)
            if not found:
                continue

            bucket, item = found
            progress = item.progress_text()

            # 下载中：推送进度
            if bucket in {"queue", "pending"} and progress and progress != last_progress:
                last_progress = progress
                try:
                    await bot.send(event, f"{source} {mode_hint}\n{progress}")
                except Exception:
                    pass

            # 下载完成
            if bucket == "done":
                error_text = item.error or str(item.extra.get("error") or item.extra.get("msg") or "")
                status = (item.status or "").lower()
                if error_text or any(w in status for w in ["error", "fail", "cancel"]):
                    try:
                        await bot.send(event, f"{source} {mode_hint}\n下载失败")
                    except Exception:
                        pass
                else:
                    msg = f"{source} {mode_hint}\n下载完成"
                    if item.filename:
                        msg += f"\n{item.filename}"
                    try:
                        await bot.send(event, msg)
                    except Exception:
                        pass
                return

    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.warning(f"Progress monitor error: {e}")
    finally:
        PROGRESS_TASKS.pop(url, None)


@metube_handler.handle()
async def handle_message(bot: Bot, event: Event):
    _cleanup_expired_users()
    text = get_text(event)
    user_key = get_user_key(event)

    # 触发等待模式
    if text == str(plugin_config.simple_command):
        loop = asyncio.get_running_loop()
        WAITING_USERS[user_key] = loop.time()
        await metube_handler.finish("继续")

    # 非等待状态，忽略
    if user_key not in WAITING_USERS:
        return

    # 检查是否超时
    loop = asyncio.get_running_loop()
    elapsed = loop.time() - WAITING_USERS[user_key]
    if elapsed > WAIT_TIMEOUT:
        del WAITING_USERS[user_key]
        await metube_handler.finish("超时，请重新发送指令")

    # 解析请求
    WAITING_USERS.pop(user_key, None)

    try:
        payload, source, mode_hint = parse_request(text)
        async with MeTubeClient() as client:
            await client.add_task(payload)
    except FinishedException:
        raise
    except RequestParseError as e:
        logger.info(f"Invalid request: {e}")
        await metube_handler.finish("错")
    except Exception as e:
        logger.error(f"MeTube add task failed: {e}")
        await metube_handler.finish("错")

    # 启动后台进度监控
    if plugin_config.progress_enabled:
        existing = PROGRESS_TASKS.get(payload.url)
        if existing and not existing.done():
            existing.cancel()
        PROGRESS_TASKS[payload.url] = asyncio.create_task(
            monitor_progress(bot, event, payload.url, source, mode_hint)
        )

    await metube_handler.send(f"已识别：{source}\n{mode_hint}")
    await metube_handler.finish("好了")
