FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Piper TTS（可通过 PIPER_BIN 环境变量覆盖路径）
RUN curl -L -o /usr/local/bin/piper \
    https://github.com/rhasspy/piper/releases/download/v1.0.0/piper_linux_amd64 && \
    chmod +x /usr/local/bin/piper

# 复制应用代码
COPY server/ /app/

WORKDIR /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 默认环境变量（可通过 docker-compose 或环境变量覆盖）
ENV MAX_TEXT_LENGTH=1000
ENV PIPER_BIN=/usr/local/bin/piper

EXPOSE 5001

CMD ["python", "app.py"]