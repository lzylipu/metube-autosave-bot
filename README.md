# MeTube Telegram Bot

<div align="center">

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/lzylipu/metube-autosave-bot.svg)](./LICENSE)
[![Docker](https://img.shields.io/docker/pulls/lzylipu/metubebot)](https://hub.docker.com/r/lzylipu/metubebot)

**极简视频下载 Telegram 机器人**

</div>

---

## 简介

基于 [NoneBot2](https://v2.nonebot.dev/) 的 Telegram 机器人，配合 [MeTube](https://github.com/alexta69/metube) 实现 YouTube、B站等视频自动下载。

**特点**：
- 支持 YouTube、B站、等多平台
- 视频音频模式切换
- 自动识别链接来源
- 进度推送通知

---

## 快速开始

### Docker 部署

```bash
docker run -d \
  --name metubebot \
  -e SUPERUSER="你的Telegram用户ID" \
  -e TELEGRAM_BOT_TOKEN="你的Bot Token" \
  -e METUBE_ENDPOINT="http://你的MeTube地址:8081" \
  --restart unless-stopped \
  lzylipu/metubebot:latest
```

### Docker Compose

```yaml
services:
  metubebot:
    image: lzylipu/metubebot:latest
    container_name: metubebot
    environment:
      SUPERUSER: "你的Telegram用户ID"
      TELEGRAM_BOT_TOKEN: "你的Bot Token"
      METUBE_ENDPOINT: "http://metube:8081"
    restart: unless-stopped
```

---

## 环境变量

| 变量 | 必填 | 说明 |
|------|:----:|------|
| `TELEGRAM_BOT_TOKEN` | ✓ | Bot Token（从 [@BotFather](https://t.me/BotFather) 获取）|
| `SUPERUSER` | ✓ | 用户 ID（从 [@userinfobot](https://t.me/userinfobot) 获取）|
| `METUBE_ENDPOINT` | ✓ | MeTube 服务地址 |
| `SIMPLE_COMMAND` | | 触发指令，默认 `1` |
| `PROGRESS_ENABLED` | | 进度推送，默认 `true` |

---

## 使用方法

### 模式说明

| 输入格式 | 下载内容 |
|---------|---------|
| `链接 1` | 最清晰视频 |
| `链接 2` | MP3 音频 |

### 示例

```
你：1
机器人：继续
你：https://www.youtube.com/watch?v=xxxxx 1
机器人：已识别：YouTube 模式1 视频
机器人：好了
```

```
你：1
机器人：继续
你：https://www.bilibili.com/video/BVxxxxx 2
机器人：已识别：B站 模式2 音频
机器人：好了
```

---

## 支持平台

- YouTube (`youtube.com`, `youtu.be`)
- B站 (`bilibili.com`, `b23.tv`)
- 其他 `yt-dlp` 支持的站点

---

## 重要设置

在 [@BotFather](https://t.me/BotFather) 执行 `/setprivacy` → 选择机器人 → `Disable`，关闭隐私模式。

---

## 致谢

- [alexta69/metube](https://github.com/alexta69/metube) - 下载后端
- [fllesser/nonebot-plugin-quark-autosave](https://github.com/fllesser/nonebot-plugin-quark-autosave) - 项目参考
- [NoneBot2](https://v2.nonebot.dev/) - 机器人框架

## 许可证

[MIT License](./LICENSE)
