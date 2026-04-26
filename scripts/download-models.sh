#!/bin/bash

# 仅用于在有代理的环境中准备或更新模型
# 生产服务器不需要执行此脚本
# 正常部署直接 git clone 即可

mkdir -p server/voices/zh_CN server/voices/en_US

echo "下载中文语音模型..."
curl -L -o server/voices/zh_CN/zh_CN-huayan-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx

curl -L -o server/voices/zh_CN/zh_CN-huayan-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json

echo "下载英文语音模型..."
curl -L -o server/voices/en_US/en_US-lessac-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx

curl -L -o server/voices/en_US/en_US-lessac-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

echo "下载完成！"