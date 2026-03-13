# quark-autosave-bot

<div align="center">
    <a href="https://github.com/lzylipu/quark-autosave-bot">
        <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo">
    </a>
    <p>✨ 一个极简的 MeTube Telegram 下载机器人 ✨</p>

[![Python Version](https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/lzylipu/quark-autosave-bot.svg)](./LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/lzylipu/quarkbot)](https://hub.docker.com/r/lzylipu/quarkbot)

</div>

## 📖 项目介绍

**quark-autosave-bot** 继续保留原有的 NoneBot2 + Telegram 机器人框架与 Docker 构建方式，但后端已切换为 [MeTube](https://github.com/alexta69/metube)。机器人专门用于把 TG 私聊中的视频链接提交到 MeTube 下载队列。

本版本特性：

- 保留原项目基本框架与 GitHub Docker 构建友好性
- 触发逻辑仍然是 `1 -> 继续 -> 链接+空格+模式`
- 更严格的链接校验
- 自动识别 **B站 / YouTube / 通用链接** 并给出提示
- 成功调用 MeTube 后回复 `好了`
- 失败统一回复 `错`
- 可选轮询 `GET /history` 自动推送下载进度与完成消息

## ✨ 模式说明

| 用户输入 | 对应参数 |
| :--- | :--- |
| `视频链接 1` | `quality=best`, `format=any` |
| `视频链接 2` | `quality=best`, `format=mp3` |

除上述字段外，其余参数都保持 MeTube 默认值，并且任务会立即开始（`auto_start=true`）。

## 🔍 链接识别规则

机器人会自动识别来源并在提交成功后提示：

- `YouTube`：如 `youtube.com`、`youtu.be`
- `B站`：如 `bilibili.com`、`b23.tv`
- `通用链接`：其他 `http/https` 视频页面链接

同时增加了更严格的基础校验：

- 只接受 `http` / `https`
- 必须有合法域名
- 不接受 `localhost` / `127.0.0.1`
- 不接受明显的图片、文本、PDF 等静态资源链接
- 必须按 `链接 空格 1/2` 的格式发送

## 🎯 工作流程

| 步骤 | 操作方 | 动作 | 说明 |
|:----:|:------:|:-----|:-----|
| **1** | **用户** | 发送指令 `1` | 启动一次下载流程 |
| **2** | **机器人** | 回复 `继续` | 提示用户下一步 |
| **3** | **用户** | 发送 `视频链接 1` 或 `视频链接 2` | 例如 `https://www.youtube.com/watch?v=xxxxx 1` |
| **4** | **机器人** | 调用 MeTube `POST /add` | 提交下载任务并立即开始 |
| **5** | **机器人** | 提示已识别来源和模式 | 例如 `已识别：YouTube / 模式1 视频` |
| **6** | **机器人** | 回复 `好了` 或 `错` | `好了` 表示提交成功，`错` 表示提交失败 |
| **7** | **机器人** | 可选进度推送 | 根据 `GET /history` 轮询发送进度或完成通知 |

## 💿 快速开始

### 🐳 使用 Docker (推荐)

**前提条件**：
1. 一个可访问的 MeTube 服务实例。
2. 一个 Telegram Bot Token（通过 [@BotFather](https://t.me/BotFather) 创建）。
3. 你的 Telegram 用户ID（通过 [@userinfobot](https://t.me/userinfobot) 获取）。

> `METUBE_ENDPOINT` **不写死**，通过 Docker 环境变量自定义。

### 运行容器

```bash
docker run -d \
  --name quarkbot \
  -e PORT=8080 \
  -e SUPERUSER="你的Telegram用户ID" \
  -e TELEGRAM_BOT_TOKEN="你的Bot Token" \
  -e METUBE_ENDPOINT="http://10.10.0.2:8081" \
  --restart unless-stopped \
  lzylipu/quarkbot:latest
```

### 使用 Docker Compose

```yaml
services:
  quarkbot:
    image: lzylipu/quarkbot:latest
    container_name: quarkbot
    environment:
      PORT: 8080
      SUPERUSER: "你的Telegram用户ID"
      TELEGRAM_BOT_TOKEN: "你的Bot Token"
      METUBE_ENDPOINT: "http://10.10.0.2:8081"
      SIMPLE_COMMAND: "1"
      PROGRESS_ENABLED: "true"
      PROGRESS_INTERVAL_SECONDS: "5"
      PROGRESS_TIMEOUT_SECONDS: "1800"
    restart: unless-stopped
```

然后运行：

```bash
docker compose up -d
```

## ⚙️ 环境变量配置

| 变量名 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | **是** | 无 | Telegram Bot Token |
| `SUPERUSER` | **是** | 无 | 允许使用机器人的 Telegram 用户ID |
| `METUBE_ENDPOINT` | 否 | `http://metube:8081` | MeTube 服务地址，推荐在部署时显式传入 |
| `PORT` | 否 | `8080` | NoneBot2 服务端口 |
| `SIMPLE_COMMAND` | 否 | `1` | 触发机器人的指令 |
| `PROGRESS_ENABLED` | 否 | `true` | 是否启用下载进度轮询和完成提示 |
| `PROGRESS_INTERVAL_SECONDS` | 否 | `5` | 轮询 MeTube 历史状态的间隔秒数 |
| `PROGRESS_TIMEOUT_SECONDS` | 否 | `1800` | 进度轮询超时时间 |

## 📝 重要：Telegram Bot 设置

为了让机器人能够响应 `1` 这样的普通文本消息，你需要在 [@BotFather](https://t.me/BotFather) 处**关闭机器人的隐私模式**：

1. 向 BotFather 发送 `/setprivacy`。
2. 选择你的机器人。
3. 选择 `Disable`。

否则，机器人只能响应以 `/` 开头的命令。

## 🚀 使用示例

### 视频模式

> **你**：`1`  
> **机器人**：`继续`  
> **你**：`https://www.youtube.com/watch?v=dQw4w9WgXcQ 1`  
> **机器人**：`已识别：YouTube` `模式1 视频`  
> **机器人**：`好了`  
> **机器人**：`YouTube 模式1 视频\n进度 42%` *(如果拿得到进度)*  
> **机器人**：`YouTube 模式1 视频\n下载完成`

### 音频模式

> **你**：`1`  
> **机器人**：`继续`  
> **你**：`https://www.bilibili.com/video/BV1xx411c7mD 2`  
> **机器人**：`已识别：B站` `模式2 音频`  
> **机器人**：`好了`

### 失败场景

> **你**：`1`  
> **机器人**：`继续`  
> **你**：`not-a-url 1`  
> **机器人**：`错`

## ❓ 常见问题

**Q: 机器人运行了，但没有任何响应？**  
A: 请按以下顺序排查：
1. 确认 `SUPERUSER` 配置的是正确的数字ID。
2. 确认已在 BotFather 处关闭了隐私模式（`/setprivacy -> Disable`）。
3. 确认服务器网络可以正常访问 Telegram API。

**Q: 总是返回“错”，但 MeTube 页面正常？**  
A: 请检查：
1. `METUBE_ENDPOINT` 是否填写正确。
2. MeTube 是否能直接访问该视频链接。
3. 目标站点是否需要 cookies、代理或额外 `yt-dlp` 配置。
4. 你发送的内容是否符合 `链接 空格 1/2` 的格式。

**Q: 为什么机器人回复“好了”，但没有马上下载完成？**  
A: `好了` 表示任务已经成功提交到 MeTube，并不是文件已经下载结束。下载是否成功、是否需要转码、是否受站点限制，取决于 MeTube 当前配置和 `yt-dlp` 实际执行情况。

**Q: 为什么有时没有进度消息？**  
A: 进度消息依赖 MeTube `GET /history` 返回的实时字段，不同站点、不同下载阶段、不同 MeTube/yt-dlp 行为下，进度信息可能不总是完整可见；但提交和完成消息不受影响。

## 🙏 致谢

* [alexta69/metube](https://github.com/alexta69/metube) - 提供下载后端与 API。
* [fllesser/nonebot-plugin-quark-autosave](https://github.com/fllesser/nonebot-plugin-quark-autosave) - 原始插件基础。
* [NoneBot2](https://v2.nonebot.dev/) - 优雅的跨平台机器人框架。

## 📄 许可证

本项目采用 [MIT License](./LICENSE) 开源。
