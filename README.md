# BrowserTTS v2

> 浏览器文字转语音 - 完全离线版 v2

## 特性

- 🐳 **Docker 部署** - 一键启动服务
- 🌐 **网页入口** - 直接访问 http://localhost:5001 即可使用
- 🔇 **完全离线** - 使用 Piper TTS，无需联网
- 🎵 **中英混合** - 自动识别并处理中英文混合文本
- ⚡ **语速可调** - 0.5x ~ 2.0x 实时调整
- 📥 **直接播放 + 下载** - MP3 格式，44.1kHz 立体声 128kbps

## 部署策略（中国网络环境）

本项目已将 Piper 模型文件直接存储在 Git 仓库中。

部署步骤：

1. **直接拉取代码**
   ```bash
   git clone https://github.com/EvanZhaoi/BrowserTTS-v2.git
   ```

2. **启动服务**
   ```bash
   docker-compose up -d --build
   ```

3. **访问网页**
   http://localhost:5001

> 无需访问 HuggingFace 或 Git LFS，模型文件已随代码一起下载。

---

## 快速开始（开发者）

### 模型文件验证

克隆后验证模型文件是真实文件（而非 LFS pointer）：

```bash
ls -lh server/voices/zh_CN/
```

- **正确情况**：文件大小约 50~70MB
- **错误情况**：只有几百字节（说明还是 LFS pointer，需重新拉取）

### 在有代理的电脑上准备/更新模型

```bash
# 创建模型目录
mkdir -p server/voices/zh_CN server/voices/en_US

# 下载中文模型 (约 60MB)
curl -L -o server/voices/zh_CN/zh_CN-huayan-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx

curl -L -o server/voices/zh_CN/zh_CN-huayan-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json

# 下载英文模型 (约 60MB)
curl -L -o server/voices/en_US/en_US-lessac-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx

curl -L -o server/voices/en_US/en_US-lessac-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

# 提交到 Git
git add server/voices/
git commit -m "Update Piper voice models"
git push
```

---

## 模型存储说明

当前模型约 92MB（中英文各一个），直接存储在 Git 仓库中。

如果未来模型增多导致仓库过大，可以考虑：

- **Git LFS** - Git 官方的二进制大文件管理方案
- **私有对象存储** - OSS、MinIO 等
- **Harbor 镜像内置模型** - 构建包含模型的 Docker 镜像
- **内网文件服务器** - 通过 URL 或 volume 挂载提供模型

---

## 架构兼容性

> ⚠️ 当前 Dockerfile 默认下载的是 `piper_linux_amd64`，适用于 amd64/x86_64 Linux 服务器。

如果部署到以下环境，需要替换为对应架构的 Piper 可执行文件：

| 架构 | 示例环境 | 解决方案 |
|------|----------|----------|
| ARM64 (aarch64) | 树莓派、ARM 服务器 | 使用 `piper_linux_aarch64` 或从源码编译 |
| Apple Silicon | Mac M1/M2/M3 | 手动安装支持 arm64 的 Piper 版本，或使用 Docker 镜像 |

可通过设置环境变量 `PIPER_BIN` 覆盖默认路径，例如：
```yaml
environment:
  - PIPER_BIN=/custom/path/piper
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
│   ├── requirements.txt     # Python 依赖
│   ├── static/
│   │   └── index.html      # 网页入口
│   └── voices/              # 语音模型（直接存储在 Git 中）
│       ├── zh_CN/
│       └── en_US/
├── scripts/
│   └── download-models.sh   # 模型下载脚本（仅用于有代理的电脑）
├── docker-compose.yml
└── README.md
```

## 部署目标

✅ 中国服务器无需外网  
✅ git clone 后直接可用  
✅ docker-compose 一键启动  
✅ 网页直接使用  
✅ 无 LFS 依赖