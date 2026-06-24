<div align="center">

# 🎬 MeTube AutoSave Bot

**Telegram Bot for MeTube Auto-Download**

Send a link, auto-download video/audio — YouTube, Bilibili, 1000+ sites 🚀

[![Python](https://img.shields.io/badge/python-3.12-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![NoneBot2](https://img.shields.io/badge/NoneBot2-2.4+-orange.svg?style=flat-square)](https://v2.nonebot.dev/)
[![Docker](https://img.shields.io/docker/pulls/lzylipu/metubebot?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/r/lzylipu/metubebot)
[![License](https://img.shields.io/github/license/lzylipu/metube-autosave-bot?style=flat-square)](./LICENSE)
[![GitHub](https://img.shields.io/badge/_repo-metube--autosave--bot-181717.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/lzylipu/metube-autosave-bot)

English · [简体中文](./README.md)

</div>

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [📋 Download Modes](#-download-modes)
- [📂 Project Structure](#-project-structure)
- [🔄 How It Works](#-how-it-works)
- [🚀 Quick Start](#-quick-start)
  - [🐳 Docker](#-docker)
  - [📦 Docker Compose](#-docker-compose)
- [⚙️ Environment Variables](#️-environment-variables)
- [💬 Chat Example](#-chat-example)
- [🌐 Supported Platforms](#-supported-platforms)
- [🔧 BotFather Setup](#-botfather-setup)
- [🛠️ Tech Stack](#️-tech-stack)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-license)

---

## ✨ Features

- 🎥 **Video Download** — Supports YouTube, Bilibili and 1000+ sites (powered by yt-dlp)
- 🎵 **Audio Extraction** — One-click MP3 extraction at best quality
- 📊 **Real-time Progress** — Download progress pushed to Telegram in real time
- 🤖 **Telegram Native** — Conversational interaction with two download modes
- 🐳 **Docker One-Command Deploy** — Image `lzylipu/metubebot:latest`, up in 30 seconds
- ⏱ **Timeout Guard** — 60s idle timeout for waiting state; configurable download timeout
- 🔁 **Auto Retry** — Built-in httpx retry mechanism for network resilience
- 🔒 **Access Control** — Only the Superuser can trigger the bot

---

## 📋 Download Modes

| Mode | Description | Output |
|:----:|-------------|--------|
| `1` | **Video** 🎥 | Best quality video (yt-dlp `best`) |
| `2` | **Audio** 🎵 | MP3 format at best quality |

---

## 📂 Project Structure

```
metube-autosave-bot/
├── 📄 bot.py                          # 🤖 NoneBot2 entry point, registers Telegram adapter
├── 🐳 Dockerfile                      # Docker image definition (Python 3.12-slim)
├── 📦 compose.yml                     # Docker Compose orchestration (Bot service)
├── ⚙️ .env.example                    # Environment variable template
├── 🔧 start.sh                        # Container startup script, generates .env.prod
├── 📄 pyproject.toml                  # Project metadata and dependencies
├── 📜 LICENSE                         # MIT License
├── 📖 README.md                       # Chinese documentation
├── 📖 README_EN.md                    # English documentation
├── 📁 .github/
│   └── workflows/
│       └── docker-publish.yml          # GitHub Actions Docker publish workflow
└── 📁 src/
    └── nonebot_plugin_metube_autosave/
        ├── __init__.py                # Plugin main logic: command trigger → download → progress push
        ├── client.py                  # MeTube API async client (with retry)
        ├── config.py                  # Pydantic configuration model
        ├── model.py                   # Data models: AddTaskPayload / DownloadItem / HistoryResponse
        └── exception.py               # Custom exception: MeTubeException
```

---

## 🔄 How It Works

```
User sends command "1" ──→ Bot enters waiting-for-link state
                            │
User sends "link 1" ──→ Validate URL & parse mode
                            │         │
                      Mode 1=Video  Mode 2=Audio 🎵
                            │
                      Submit to MeTube service
                            │
                      Monitor download progress in background
                            │
                      Push real-time progress to TG ──→ Download complete/fail notification ✅
```

---

## 🚀 Quick Start

### 🐳 Docker

```bash
docker run -d \
  --name metubebot \
  --network host \
  -e TELEGRAM_BOT_TOKEN=*** \
  -e SUPERUSER="your_telegram_user_id" \
  -e METUBE_ENDPOINT="http://your-metube-address:8081" \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  lzylipu/metubebot:latest
```

> ⚠️ The bot uses `network_mode: host` to ensure MeTube service reachability.

### 📦 Docker Compose

```bash
cp .env.example .env   # Edit .env with your configuration
docker compose up -d
```

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|----------|:--------:|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | | Telegram Bot Token from [@BotFather](https://t.me/BotFather) |
| `SUPERUSER` | ✅ | | Telegram User ID from [@userinfobot](https://t.me/userinfobot) |
| `METUBE_ENDPOINT` | ✅ | `http://metube:8081` | MeTube service address |
| `SIMPLE_COMMAND` | | `1` | Trigger command, customizable (e.g. `dl`, `下`) |
| `PROGRESS_ENABLED` | | `true` | Enable download progress notifications |
| `PROGRESS_INTERVAL_SECONDS` | | `5` | Progress push refresh interval (seconds), minimum 2 |
| `PROGRESS_TIMEOUT_SECONDS` | | `1800` | Progress monitoring timeout (seconds), minimum 30 |

---

## 💬 Chat Example

**Video Download 🎥**

```
You:  1
Bot:  Go ahead

You:  https://www.youtube.com/watch?v=dQw4w9WgXcQ 1
Bot:  Identified: YouTube
      Video
Bot:  YouTube Video
      📊 Progress: 45.2%
Bot:  YouTube Video
      📊 Progress: 89.7%
Bot:  YouTube Video
      Download complete
      Rick Astley - Never Gonna Give You Up.mp4
```

**Audio Extraction 🎵**

```
You:  1
Bot:  Go ahead

You:  https://www.bilibili.com/video/BV1xx 2
Bot:  Identified: Bilibili
      Audio
Bot:  Bilibili Audio
      Download complete
      some_video.mp3
```

> ⏱ If no link is sent within 60 seconds, the waiting state expires automatically.

---

## 🌐 Supported Platforms

- 🟥 **YouTube** — `youtube.com`, `youtu.be`, `music.youtube.com`
- 📺 **Bilibili** — `bilibili.com`, `b23.tv`
- 🌍 **1000+ Sites** — [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

> MeTube uses the yt-dlp engine under the hood, supporting all its compatible sites.

---

## 🔧 BotFather Setup

For the bot to read **all messages** you send (not just `/` commands), you need to disable privacy mode in BotFather:

1. Open [@BotFather](https://t.me/BotFather) 🤖
2. Send `/setprivacy`
3. Select your Bot
4. Select **Disable** 🔓

---

## 🛠️ Tech Stack

| Component | Version / Description |
|-----------|----------------------|
| 🐍 Python | 3.12 |
| 🤖 [NoneBot2](https://v2.nonebot.dev/) | Async bot framework (FastAPI + httpx driver) |
| 📡 [nonebot-adapter-telegram](https://github.com/nonebot/adapter-telegram) | Telegram adapter |
| 🌐 [httpx](https://www.python-httpx.org/) | Async HTTP client (keepalive + auto-retry) |
| 📺 [MeTube](https://github.com/alexta69/metube) | YouTube-dl frontend service |
| ⬇️ [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download engine (1000+ site support) |

---

## 🙏 Acknowledgements

- 📺 [alexta69/metube](https://github.com/alexta69/metube) — MeTube download service
- ⬇️ [yt-dlp](https://github.com/yt-dlp/yt-dlp) — Download engine
- 🤖 [NoneBot2](https://v2.nonebot.dev/) — Async bot framework

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).
