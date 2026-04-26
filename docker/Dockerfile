FROM python:3.11-slim

# 替换为阿里云镜像源加速 apt 下载
RUN sed -i 's|http://deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list || true && \
    sed -i 's|http://security.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list || true && \
    sed -i 's|http://deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources || true && \
    sed -i 's|http://security.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources || true

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制 Piper（包含二进制和依赖库）
COPY docker/bin/piper_linux_amd64/ /usr/local/piper/

RUN chmod +x /usr/local/piper/piper && \
    chmod -R 755 /usr/local/piper

# 复制应用代码
COPY server/ /app/

WORKDIR /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 默认环境变量（可通过 docker-compose 或环境变量覆盖）
ENV MAX_TEXT_LENGTH=1000
ENV PIPER_BIN=/usr/local/piper/piper

EXPOSE 5001

CMD ["python", "app.py"]