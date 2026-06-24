<div align="center">

# 🎬 MeTube AutoSave Bot

**Telegram Bot · Send a link, auto-download video/audio — YouTube, Bilibili, 1000+ sites**

[![Python](https://img.shields.io/badge/python-3.12-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![NoneBot2](https://img.shields.io/badge/NoneBot2-2.4+-orange.svg?style=flat-square)](https://v2.nonebot.dev/)
[![Docker](https://img.shields.io/docker/pulls/lzylipu/metubebot?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/r/lzylipu/metubebot)
[![License](https://img.shields.io/github/license/lzylipu/metube-autosave-bot?style=flat-square)](./LICENSE)
[![GitHub](https://img.shields.io/badge/_repo-metube--autosave--bot-181717.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/lzylipu/metube-autosave-bot)

简体中文 · [English](./README.en.md)

</div>

---

## 📖 Table of Contents

- [Features](#-features)
- [Download Modes](#-download-modes)
- [How It Works](#-how-it-works)
- [Quick Start](#-quick-start)
  - [Docker](#-docker)
  - [Docker Compose](#-docker-compose)
- [Environment Variables](#-environment-variables)
- [Chat Example](#-chat-example)
- [Supported Platforms](#-supported-platforms)
- [BotFather Setup](#-botfather-setup)
- [Tech Stack](#-tech-stack)
- [Acknowledgements](#-acknowledgements)
- [License](#-license)

---

## ✨ Features

- 🎥 **Video Download** — Supports YouTube, Bilibili and 1000+ sites (powered by yt-dlp)
- 🎵 **Audio Extraction** — One-click MP3 extraction at best quality
- 📊 **Real-time Progress** — Download progress pushed to Telegram in real time
- 🤖 **Telegram Native** — Conversational interaction with two download modes
- 🐳 **Docker One-Command Deploy** — Image `lzylipu/metubebot:latest`, up in 30 seconds
- ⏱ **Timeout Guard** — 60s idle timeout for waiting state; configurable download timeout

---

## 📋 Download Modes

| Mode | Description | Output |
|:----:|-------------|--------|
| `1` | **Video** | Best quality video (yt-dlp `best`) |
| `2` | **Audio** | MP3 format at highest quality |

---

## 🔄 How It Works

```
User sends "1"  ──→  Bot enters waiting state
                            │
User sends "link 1"  ──→   Validate URL & parse mode
                            │         │
                      mode 1=video  mode 2=mp3
                            │
                      Submit to MeTube service
                            │
                      Monitor download progress
                            │
                      Push progress to TG  ──→  Done / Failed notification
```

---

## 🚀 Quick Start

### 🐳 Docker

```bash
docker run -d \
  --name metubebot \
  --network host \
  -e TELEGRAM_BOT_TOKEN="your...en" \
  -e SUPERUSER="your_telegram_user_id" \
  -e METUBE_ENDPOINT="http://your-metube-host:8081" \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  lzylipu/metubebot:latest
```

> ⚠️ The bot uses `network_mode: host` — make sure the MeTube service is reachable.

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
| `SIMPLE_COMMAND` | | `1` | Trigger command, customizable (e.g. `dl`) |
| `PROGRESS_ENABLED` | | `true` | Enable download progress notifications |
| `PROGRESS_INTERVAL_SECONDS` | | `5` | Progress refresh interval (seconds), min 2 |
| `PROGRESS_TIMEOUT_SECONDS` | | `1800` | Progress monitor timeout (seconds), min 30 |

---

## 💬 Chat Example

```
You:  1
Bot:  Continue

You:  https://www.youtube.com/watch?v=dQw4w9WgXcQ 1
Bot:  Detected: YouTube
      Video
Bot:  YouTube Video
      📊 Progress: 45.2%
Bot:  YouTube Video
      📊 Progress: 89.7%
Bot:  YouTube Video
      Download complete
      Rick Astley - Never Gonna Give You Up.mp4
```

```
You:  1
Bot:  Continue

You:  https://www.bilibili.com/video/BV1xx 2
Bot:  Detected: Bilibili
      Audio
Bot:  Bilibili Audio
      Download complete
      some_video.mp3
```

> ⏱ If no link is sent within 60 seconds, the waiting state expires — send the command again.

---

## 🌐 Supported Platforms

- **YouTube** — `youtube.com`, `youtu.be`, `music.youtube.com`
- **Bilibili** — `bilibili.com`, `b23.tv`
- **1000+ sites** — [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

> MeTube uses yt-dlp as its download engine, supporting all yt-dlp compatible sites.

---

## 🔧 BotFather Setup

For the bot to read **all messages** (not just `/` commands), disable privacy mode in BotFather:

1. Open [@BotFather](https://t.me/BotFather)
2. Send `/setprivacy`
3. Select your bot
4. Choose **Disable**

---

## 🛠 Tech Stack

| Component | Version / Notes |
|-----------|----------------|
| Python | 3.12 |
| [NoneBot2](https://v2.nonebot.dev/) | Async bot framework (FastAPI + httpx driver) |
| [nonebot-adapter-telegram](https://github.com/nonebot/adapter-telegram) | Telegram adapter |
| [httpx](https://www.python-httpx.org/) | Async HTTP client (keepalive + auto-retry) |
| [MeTube](https://github.com/alexta69/metube) | YouTube-dl frontend service |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download engine (1000+ sites) |

---

## 🙏 Acknowledgements

- [alexta69/metube](https://github.com/alexta69/metube) — MeTube download service
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — Download engine
- [NoneBot2](https://v2.nonebot.dev/) — Async bot framework

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).
