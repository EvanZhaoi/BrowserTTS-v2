# BrowserTTS v2

> 浏览器文字转语音 - 完全离线版 v2

## 特性

- 🐳 **Docker 部署** - 一键启动服务
- 🔇 **完全离线** - 使用 Piper TTS，无需联网
- 🎵 **中英混合** - 自动识别并处理中英文混合文本
- ⚡ **高速转换** - 使用 ffmpeg 生成高质量 MP3

## 快速开始

### 1. 下载语音模型（重要！）

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

**提交到 Git：**
```bash
git add server/voices/
git commit -m "Add Piper TTS voice models"
git push
```

部署时拉取代码，模型已经在项目中。

### 2. 启动 Docker

```bash
docker-compose up -d
```

### 3. 测试

访问 http://localhost:5001/health 确认服务运行正常。

### 4. 安装浏览器插件

1. 打开 Chrome，访问 `chrome://extensions/`
2. 开启右上角「开发者模式」
3. 点击「加载已解压的扩展程序」
4. 选择 `extension/` 文件夹

使用方法：选中网页文字 → 右键 → "保存为音频"

### 5. 使用网页工具

```bash
cd web
npm install
npm run dev
```

访问 http://localhost:3000

## API 接口

### POST /speak

```json
{
  "text": "Hello你好World世界",
  "rate": 1.0
}
```

- `text`: 要转换的文字（建议不超过500字）
- `rate`: 语速，0.5=慢速，1.0=正常，2.0=快速

### GET /health

返回服务状态。

## 输出规格

- 格式：MP3
- 采样率：44.1kHz
- 声道：立体声
- 比特率：128kbps

## 技术栈

- Piper TTS - 离线神经网络TTS
- ffmpeg - 音频处理
- Flask - Web服务
- Vue 3 + Vite - 网页前端
- Docker - 容器化部署

## 部署说明

1. 在有代理的机器上运行 `scripts/download-models.sh` 下载模型
2. 提交到 Git：`git add server/voices/`
3. 在目标服务器 `git clone` 或 `git pull`
4. 运行 `docker-compose up -d`

模型文件约 92MB（中英文各一个模型）。
