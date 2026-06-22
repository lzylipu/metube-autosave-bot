# MeTube AutoSave Bot

<div align="center">

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/lzylipu/metube-autosave-bot.svg)](./LICENSE)
[![Docker](https://img.shields.io/docker/pulls/lzylipu/metubebot)](https://hub.docker.com/r/lzylipu/metubebot)

**Minimal Telegram bot for video/audio download via MeTube**

</div>

---

## Features

- **One-tap download**: Send `1` -> link + mode -> done
- **Multi-platform**: YouTube, Bilibili, and 1000+ yt-dlp supported sites
- **Video/Audio modes**: Mode `1` = best video, Mode `2` = MP3 audio
- **Progress tracking**: Real-time download progress notifications
- **Privacy-first**: Only responds to configured superuser

## Quick Start

### Docker

```bash
docker run -d \
  --name metubebot \
  -e SUPERUSER="your" \
  -e TELEGRAM_BOT_TOKEN=*** \
  -e METUBE_ENDPOINT="http://your:8081" \
  --restart unless-stopped \
  lzylipu/metubebot:latest
```

### Docker Compose

```bash
cp .env.example .env  # fill in your values
docker compose up -d
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|:--------:|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | yes | | Bot token from [@BotFather](https://t.me/BotFather) |
| `SUPERUSER` | yes | | Your Telegram user ID from [@userinfobot](https://t.me/userinfobot) |
| `METUBE_ENDPOINT` | yes | | MeTube service URL |
| `SIMPLE_COMMAND` | | `1` | Trigger command |
| `PROGRESS_ENABLED` | | `true` | Enable progress notifications |
| `PROGRESS_INTERVAL_SECONDS` | | `5` | Progress poll interval |
| `PROGRESS_TIMEOUT_SECONDS` | | `1800` | Progress monitor timeout |

## Usage

| Input | Action |
|-------|--------|
| `link 1` | Download best quality video |
| `link 2` | Download as MP3 audio |

```
You: 1
Bot: continue
You: https://www.youtube.com/watch?v=xxxxx 1
Bot: YouTube mode1 video
Bot: done
```

## Supported Platforms

- YouTube (`youtube.com`, `youtu.be`)
- Bilibili (`bilibili.com`, `b23.tv`)
- Any site supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Setup

Disable privacy mode in [@BotFather](https://t.me/BotFather): `/setprivacy` -> select bot -> `Disable`.

## Credits

- [alexta69/metube](https://github.com/alexta69/metube) - Download backend
- [NoneBot2](https://v2.nonebot.dev/) - Bot framework

## License

[MIT](./LICENSE)
