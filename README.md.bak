<div align="center">

# 🎬 MeTube AutoSave Bot

**MeTube 自动转存 Telegram 机器人**

发链接自动下载视频/音频，YouTube、B站、1000+ 网站通吃 🚀

[![Python](https://img.shields.io/badge/python-3.12-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![NoneBot2](https://img.shields.io/badge/NoneBot2-2.4+-orange.svg?style=flat-square)](https://v2.nonebot.dev/)
[![Docker](https://img.shields.io/docker/pulls/lzylipu/metubebot?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/r/lzylipu/metubebot)
[![License](https://img.shields.io/github/license/lzylipu/metube-autosave-bot?style=flat-square)](./LICENSE)
[![GitHub](https://img.shields.io/badge/_repo-metube--autosave--bot-181717.svg?style=flat-square&logo=github&logoColor=white)](https://github.com/lzylipu/metube-autosave-bot)

[English](./README_EN.md) · 简体中文

</div>

---

## 📖 目录

- [✨ 功能特性](#-功能特性)
- [📋 下载模式](#-下载模式)
- [📂 项目结构](#-项目结构)
- [🔄 工作流程](#-工作流程)
- [🚀 快速开始](#-快速开始)
  - [🐳 Docker](#-docker)
  - [📦 Docker Compose](#-docker-compose)
- [⚙️ 环境变量](#️-环境变量)
- [💬 聊天示例](#-聊天示例)
- [🌐 支持的平台](#-支持的平台)
- [🔧 BotFather 配置](#-botfather-配置)
- [🛠️ 技术栈](#️-技术栈)
- [🙏 致谢](#-致谢)
- [📄 许可证](#-许可证)

---

## ✨ 功能特性

- 🎥 **视频下载** — 支持 YouTube、B站等 1000+ 网站（基于 yt-dlp）
- 🎵 **音频提取** — 一键提取 MP3，最高音质
- 📊 **实时进度** — 下载进度实时推送到 Telegram
- 🤖 **Telegram 原生交互** — 对话式操作，两种模式自由切换
- 🐳 **Docker 一键部署** — 镜像 `lzylipu/metubebot:latest`，30 秒上线
- ⏱ **超时保护** — 60 秒无操作自动退出等待状态；下载超时可配
- 🔁 **自动重试** — 内置 httpx 重试机制，网络波动自动恢复
- 🔒 **权限控制** — 仅 Superuser 可触发，安全可控

---

## 📋 下载模式

| 模式 | 说明 | 输出 |
|:----:|------|------|
| `1` | **视频模式** 🎥 | 最高画质视频（yt-dlp `best`） |
| `2` | **音频模式** 🎵 | MP3 格式音频（最高音质） |

---

## 📂 项目结构

```
metube-autosave-bot/
├── 📄 bot.py                          # 🤖 NoneBot2 入口，注册 Telegram 适配器
├── 🐳 Dockerfile                      # Docker 镜像定义（Python 3.12-slim）
├── 📦 compose.yml                     # Docker Compose 编排（Bot 服务）
├── ⚙️ .env.example                    # 环境变量示例文件
├── 🔧 start.sh                        # 容器启动脚本，生成 .env.prod
├── 📄 pyproject.toml                  # 项目元数据与依赖声明
├── 📜 LICENSE                         # MIT 开源许可证
├── 📖 README.md                       # 中文说明文档
├── 📖 README_EN.md                    # 英文说明文档
├── 📁 .github/
│   └── workflows/
│       └── docker-publish.yml          # GitHub Actions Docker 发布流程
└── 📁 src/
    └── nonebot_plugin_metube_autosave/
        ├── __init__.py                # 插件主逻辑：指令触发 → 下载流程 → 进度推送
        ├── client.py                  # MeTube API 异步客户端（带重试）
        ├── config.py                  # Pydantic 配置模型
        ├── model.py                   # 数据模型：AddTaskPayload / DownloadItem / HistoryResponse
        └── exception.py               # 自定义异常 MeTubeException
```

---

## 🔄 工作流程

```
用户发送指令 "1" ──→ Bot 进入等待链接状态
                          │
用户发送 "链接 1" ──→ 验证 URL & 解析模式
                          │         │
                    模式1=视频  模式2=音频 🎵
                          │
                    提交给 MeTube 服务
                          │
                    后台监控下载进度
                          │
                    实时推送进度到 TG ──→ 下载完成/失败通知 ✅
```

---

## 🚀 快速开始

### 🐳 Docker

```bash
docker run -d \
  --name metubebot \
  --network host \
  -e TELEGRAM_BOT_TOKEN=*** \
  -e SUPERUSER="你的TG用户ID" \
  -e METUBE_ENDPOINT="http://你的MeTube地址:8081" \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  lzylipu/metubebot:latest
```

> ⚠️ Bot 使用 `network_mode: host`，确保 MeTube 服务可达。

### 📦 Docker Compose

```bash
cp .env.example .env   # 编辑 .env 填入你的配置
docker compose up -d
```

---

## ⚙️ 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|:----:|--------|------|
| `TELEGRAM_BOT_TOKEN` | ✅ | | Telegram Bot Token，从 [@BotFather](https://t.me/BotFather) 获取 |
| `SUPERUSER` | ✅ | | Telegram 用户 ID，从 [@userinfobot](https://t.me/userinfobot) 查询 |
| `METUBE_ENDPOINT` | ✅ | `http://metube:8081` | MeTube 服务地址 |
| `SIMPLE_COMMAND` | | `1` | 触发指令，可自定义（如 `dl`、`下`） |
| `PROGRESS_ENABLED` | | `true` | 是否开启下载进度通知 |
| `PROGRESS_INTERVAL_SECONDS` | | `5` | 进度推送刷新间隔（秒），最小 2 |
| `PROGRESS_TIMEOUT_SECONDS` | | `1800` | 进度监控超时（秒），最小 30 |

---

## 💬 聊天示例

**视频下载 🎥**

```
你:  1
机器人: 继续

你:  https://www.youtube.com/watch?v=dQw4w9WgXcQ 1
机器人: 已识别：YouTube
       视频
机器人: YouTube 视频
       📊 进度: 45.2%
机器人: YouTube 视频
       📊 进度: 89.7%
机器人: YouTube 视频
       下载完成
       Rick Astley - Never Gonna Give You Up.mp4
```

**音频提取 🎵**

```
你:  1
机器人: 继续

你:  https://www.bilibili.com/video/BV1xx 2
机器人: 已识别：B站
       音频
机器人: B站 音频
       下载完成
       some_video.mp3
```

> ⏱ 60 秒内未发送链接，等待状态自动过期，需重新发送指令。

---

## 🌐 支持的平台

- 🟥 **YouTube** — `youtube.com`、`youtu.be`、`music.youtube.com`
- 📺 **B站** — `bilibili.com`、`b23.tv`
- 🌍 **1000+ 网站** — [yt-dlp 支持列表](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

> MeTube 底层使用 yt-dlp 引擎，支持其所有兼容网站。

---

## 🔧 BotFather 配置

为了让 bot 能读取你发送的**所有消息**（而不仅是以 `/` 开头的命令），需要在 BotFather 中关闭隐私模式：

1. 打开 [@BotFather](https://t.me/BotFather) 🤖
2. 发送 `/setprivacy`
3. 选择你的 Bot
4. 选择 **Disable** 🔓

---

## 🛠️ 技术栈

| 组件 | 版本 / 说明 |
|------|------------|
| 🐍 Python | 3.12 |
| 🤖 [NoneBot2](https://v2.nonebot.dev/) | 异步机器人框架（FastAPI + httpx 驱动） |
| 📡 [nonebot-adapter-telegram](https://github.com/nonebot/adapter-telegram) | Telegram 适配器 |
| 🌐 [httpx](https://www.python-httpx.org/) | 异步 HTTP 客户端（keepalive + 自动重试） |
| 📺 [MeTube](https://github.com/alexta69/metube) | YouTube-dl 前端服务 |
| ⬇️ [yt-dlp](https://github.com/yt-dlp/yt-dlp) | 下载引擎（1000+ 网站支持） |

---

## 🙏 致谢

- 📺 [alexta69/metube](https://github.com/alexta69/metube) — MeTube 下载服务
- ⬇️ [yt-dlp](https://github.com/yt-dlp/yt-dlp) — 下载引擎
- 🤖 [NoneBot2](https://v2.nonebot.dev/) — 异步机器人框架

---

## 📄 许可证

本项目基于 [MIT License](./LICENSE) 开源。
