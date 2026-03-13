import asyncio
import re
from urllib.parse import urlparse

from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot.exception import FinishedException
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .client import MeTubeClient
from .config import Config, plugin_config
from .model import AddTaskPayload

__plugin_meta__ = PluginMetadata(
    name="MeTube Telegram 下载机器人",
    description="极简 TG 私聊插件：1 -> 继续 -> 视频链接+空格+模式 -> 调用 MeTube 立即下载",
    usage="发送 1 后按提示发送：视频链接 空格 1/2",
    type="application",
    homepage="https://github.com/lzylipu/quark-autosave-bot",
    config=Config,
    supported_adapters=inherit_supported_adapters(),
    extra={"author": "lzylipu / modified for MeTube"},
)

WAITING_USERS: dict[str, bool] = {}
PROGRESS_TASKS: dict[str, asyncio.Task] = {}

simple_qas = on_message(permission=SUPERUSER, block=True)

SUPPORTED_SCHEMES = {"http", "https"}
YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "music.youtube.com",
}
BILIBILI_HOSTS = {
    "bilibili.com",
    "www.bilibili.com",
    "m.bilibili.com",
    "b23.tv",
}
VIDEO_HOST_HINTS = [
    "youtube.com",
    "youtu.be",
    "bilibili.com",
    "b23.tv",
    "twitter.com",
    "x.com",
    "instagram.com",
    "tiktok.com",
    "vimeo.com",
]
INVALID_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".txt"}
MODE_HELP = "链接后需跟一个空格和模式：1=best/any，2=best/mp3"


class RequestParseError(ValueError):
    pass


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
    return "通用链接"


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
        raise RequestParseError("missing mode")
    url_part, mode = parts
    url, source = normalize_url(url_part)

    if mode == "1":
        payload = AddTaskPayload(url=url, quality="best", format="any", auto_start=True)
        mode_hint = "模式1 视频"
    elif mode == "2":
        payload = AddTaskPayload(url=url, quality="best", format="mp3", auto_start=True)
        mode_hint = "模式2 音频"
    else:
        raise RequestParseError("invalid mode")

    return payload, source, mode_hint


async def monitor_progress(bot: Bot, event: Event, url: str, source: str, mode_hint: str):
    last_progress = None
    try:
        deadline = asyncio.get_event_loop().time() + plugin_config.progress_timeout_seconds
        while asyncio.get_event_loop().time() < deadline:
            await asyncio.sleep(plugin_config.progress_interval_seconds)
            async with MeTubeClient() as client:
                history = await client.get_history()
            found = history.find_by_url(url)
            if not found:
                continue
            bucket, item = found
            progress = item.progress_text()
            if bucket in {"queue", "pending"} and progress and progress != last_progress:
                last_progress = progress
                try:
                    await bot.send(event, f"{source} {mode_hint}\n进度 {progress}")
                except Exception:
                    pass
            if bucket == "done":
                status_text = (item.status or "").lower()
                error_text = item.error or str(item.extra.get("error") or item.extra.get("msg") or "")
                if error_text or any(word in status_text for word in ["error", "fail", "cancel"]):
                    try:
                        await bot.send(event, f"{source} {mode_hint}\n下载失败")
                    except Exception:
                        pass
                else:
                    message = f"{source} {mode_hint}\n下载完成"
                    if item.filename:
                        message = f"{source} {mode_hint}\n下载完成\n{item.filename}"
                    try:
                        await bot.send(event, message)
                    except Exception:
                        pass
                return
    except Exception as e:
        print(f"[nonebot_plugin_quark_autosave] progress monitor error ({mode_hint}): {e}")
    finally:
        PROGRESS_TASKS.pop(url, None)


@simple_qas.handle()
async def _(bot: Bot, event: Event):
    text = get_text(event)
    user_key = get_user_key(event)

    if text == str(plugin_config.simple_command):
        WAITING_USERS[user_key] = True
        await simple_qas.finish("继续")

    if not WAITING_USERS.get(user_key, False):
        return

    WAITING_USERS[user_key] = False

    try:
        payload, source, mode_hint = parse_request(text)
        async with MeTubeClient() as client:
            await client.add_task(payload)
    except FinishedException:
        raise
    except RequestParseError as e:
        print(f"[nonebot_plugin_quark_autosave] invalid request: {e}")
        await simple_qas.finish("错")
    except Exception as e:
        print(f"[nonebot_plugin_quark_autosave] error: {e}")
        await simple_qas.finish("错")

    if plugin_config.progress_enabled:
        existing = PROGRESS_TASKS.get(payload.url)
        if existing and not existing.done():
            existing.cancel()
        PROGRESS_TASKS[payload.url] = asyncio.create_task(
            monitor_progress(bot, event, payload.url, source, mode_hint)
        )

    await simple_qas.send(f"已识别：{source}\n{mode_hint}")
    await simple_qas.finish("好了")
