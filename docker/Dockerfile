FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 Piper TTS
RUN curl -L -o /usr/local/bin/piper \
    https://github.com/rhasspy/piper/releases/download/v1.0.0/piper_linux_amd64 && \
    chmod +x /usr/local/bin/piper

# 复制语音模型
COPY server/voices/ /app/voices/

# 复制应用代码
COPY server/ /app/

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "app.py"]
