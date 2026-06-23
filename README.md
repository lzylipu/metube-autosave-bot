# 🎬 MeTube 自动下载器 — Telegram 机器人

> 📥 发个链接给机器人，视频/音频就到手了～ YouTube、B站、1000+网站通吃 🎉

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/lzylipu/metube-autosave-bot.svg)](./LICENSE)
[![Docker](https://img.shields.io/docker/pulls/lzylipu/metubebot)](https://hub.docker.com/r/lzylipu/metubebot)

---

## ✨ 它能做什么？

| 你发 | 机器人做 |
|------|---------|
| `1` | 进入"等链接"模式 🤖 |
| `链接 1` | 下载最高画质视频 🎥 |
| `链接 2` | 下载 MP3 音频 🎵 |
| 实时推送进度！ | 📊 下载到多少了都能看 |

---

## 🚀 跑起来（30秒）

### 🐳 Docker

```bash
docker run -d \
  --name metubebot \
  -e SUPERUSER="你的TG用户ID" \
  -e TELEGRAM_BOT_TOKEN="Bot...en" \
  -e METUBE_ENDPOINT="http://你的MeTube地址:8081" \
  --restart unless-stopped \
  lzylipu/metubebot:latest
```

### 📦 Docker Compose

```bash
cp .env.example .env   # 填配置
docker compose up -d
```

---

## ⚙️ 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|:----:|--------|------|
| `TELEGRAM_BOT_TOKEN` | ✅ | | 去 [@BotFather](https://t.me/BotFather) 注册机器人拿到 token |
| `SUPERUSER` | ✅ | | 你的 TG 用户 ID，去 [@userinfobot](https://t.me/userinfobot) 查 |
| `METUBE_ENDPOINT` | ✅ | | MeTube 服务地址（比如 `http://10.10.0.2:8081`） |
| `SIMPLE_COMMAND` | | `1` | 触发指令 |
| `PROGRESS_ENABLED` | | `true` | 开启下载进度通知 |
| `PROGRESS_INTERVAL_SECONDS` | | `5` | 进度刷新间隔（秒） |
| `PROGRESS_TIMEOUT_SECONDS` | | `1800` | 进度监控超时（秒） |

---

## 💬 聊天示例

```
你:  1
机器人: 继续，发链接和模式给我～
      格式: 链接 模式
      模式1=视频 模式2=MP3

你:  https://www.youtube.com/watch?v=xxxxx 1
机器人: ⏬ 正在下载 YouTube 视频...
机器人: 📊 进度: 65.4%
...
机器人: ✅ 下载完成！👇
       [文件已发送]
```

---

## 🌐 支持的平台

- **YouTube** — `youtube.com`、`youtu.be`
- **B站** — `bilibili.com`、`b23.tv`
- **1000+** — [yt-dlp](https://github.com/yt-dlp/yt-dlp) 支持的所有网站都行

---

## 🔧 配置小贴士

在 [@BotFather](https://t.me/BotFather) 里关掉隐私模式：
`/setprivacy` → 选你的 bot → `Disable`

这样机器人才能看到消息哦～

---

## 🙏 感谢

- [alexta69/metube](https://github.com/alexta69/metube) — MeTube 下载服务
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — 下载引擎

## 📄 License

[MIT](./LICENSE)
