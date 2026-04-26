# BrowserTTS v2

> 浏览器文字转语音 - 完全离线版 v2

## 特性

- 🐳 **Docker 部署** - 一键启动服务
- 🌐 **网页入口** - 直接访问 http://localhost:5001 即可使用
- 🔇 **完全离线** - 使用 Piper TTS，无需联网
- 🎵 **中英混合** - 自动识别并处理中英文混合文本
- ⚡ **语速可调** - 0.5x ~ 2.0x 实时调整
- 📥 **直接播放 + 下载** - MP3 格式，44.1kHz 立体声 128kbps

## 快速开始

### 1. 启动 Docker

```bash
docker-compose up -d --build
```

### 2. 访问网页

打开浏览器访问：
```
http://localhost:5001
```

即可看到网页界面，输入文字、调整语速、生成语音、在线播放或下载 MP3。

### 3. 下载语音模型（首次运行前需要）

**前提**：首次下载需要在有代理的机器上完成（因为 HuggingFace 在国内访问慢）。

```bash
# 创建模型目录
mkdir -p server/voices/zh_CN server/voices/en_US

# 下载中文模型 (约 46MB)
curl -L -o server/voices/zh_CN/zh_CN-huayan-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx

curl -L -o server/voices/zh_CN/zh_CN-huayan-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json

# 下载英文模型 (约 46MB)
curl -L -o server/voices/en_US/en_US-lessac-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx

curl -L -o server/voices/en_US/en_US-lessac-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

或者使用脚本（需要代理）：
```bash
bash scripts/download-models.sh
```

**注意**：模型文件约 92MB（中英文各一个模型），不建议提交到 Git。建议放到 `server/voices/` 目录并通过 volume 挂载持久化。

### 4. 测试 API

访问健康检查：
```bash
curl http://localhost:5001/health
```

测试语音生成：
```bash
curl -X POST http://localhost:5001/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello你好World世界", "rate": 1.0}' \
  --output test.mp3
```

## 网页功能

- **输入文字**：textarea 输入，最多 1000 字符（可通过 MAX_TEXT_LENGTH 环境变量配置）
- **调整语速**：range 滑块，0.5x ~ 2.0x，step 0.1
- **生成语音**：点击按钮生成 MP3
- **在线播放**：使用 audio 标签直接播放
- **下载 MP3**：点击下载链接保存到本地

## API 接口

### POST /speak

```json
{
  "text": "Hello你好World世界",
  "rate": 1.0
}
```

- `text`: 要转换的文字（默认最多 1000 字符）
- `rate`: 语速，0.5 = 慢速，1.0 = 正常，2.0 = 快速

返回：`audio/mpeg` (MP3 格式，44.1kHz 立体声 128kbps)

### GET /health

返回服务状态。

### GET /

返回静态网页入口（index.html）

## 输出规格

- 格式：MP3
- 采样率：44.1kHz
- 声道：立体声
- 比特率：128kbps

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MAX_TEXT_LENGTH` | `1000` | 最大文本长度 |
| `PIPER_BIN` | `/usr/local/bin/piper` | Piper 可执行文件路径 |

## 技术栈

- Piper TTS - 离线神经网络TTS
- ffmpeg - 音频处理（atempo 语速调整）
- Flask - Web服务 + 静态文件
- Docker - 容器化部署

## 项目结构

```
BrowserTTS-v2/
├── docker/
│   └── Dockerfile          # Docker 镜像配置
├── server/
│   ├── app.py               # Flask 服务端
│   ├── static/
│   │   └── index.html       # 网页入口
│   └── voices/              # 语音模型目录（需要单独下载）
│       ├── zh_CN/
│       └── en_US/
├── docker-compose.yml
├── requirements.txt
├── scripts/
│   └── download-models.sh  # 模型下载脚本
└── README.md
```