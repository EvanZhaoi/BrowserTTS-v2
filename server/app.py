# -*- coding: utf-8 -*-
"""
BrowserTTS v2 - Flask 服务端
使用 Piper TTS 进行文字转语音
"""

import io
import os
import uuid
import re
import subprocess
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# 配置
MAX_TEXT_LENGTH = int(os.environ.get('MAX_TEXT_LENGTH', '1000'))
PIPER_BIN = os.environ.get('PIPER_BIN', '/usr/local/bin/piper')

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOICES_DIR = os.path.join(BASE_DIR, 'voices')

# 模型配置
MODELS = {
    'zh': {
        'model': os.path.join(VOICES_DIR, 'zh_CN', 'zh_CN-huayan-medium.onnx'),
        'config': os.path.join(VOICES_DIR, 'zh_CN', 'zh_CN-huayan-medium.onnx.json'),
    },
    'en': {
        'model': os.path.join(VOICES_DIR, 'en_US', 'en_US-lessac-medium.onnx'),
        'config': os.path.join(VOICES_DIR, 'en_US', 'en_US-lessac-medium.onnx.json'),
    }
}


def is_chinese(text: str) -> bool:
    """判断文本是否主要为中文"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    return total_chars > 0 and chinese_chars / total_chars > 0.5


def split_text(text: str) -> list:
    """将混合文本分段"""
    segments = []

    # 修复正则：中文一段，非中文一段
    pattern = r'([\u4e00-\u9fff]+|[^\u4e00-\u9fff]+)'
    parts = re.findall(pattern, text)

    current_lang = None
    current_text = []

    for part in parts:
        part = part.strip()
        if not part:
            continue

        lang = 'zh' if is_chinese(part) else 'en'

        if lang == current_lang:
            current_text.append(part)
        else:
            if current_text:
                segments.append({
                    'lang': current_lang,
                    'text': ''.join(current_text)
                })
            current_lang = lang
            current_text = [part]

    if current_text:
        segments.append({
            'lang': current_lang,
            'text': ''.join(current_text)
        })

    return segments


def generate_audio(text: str, rate: float = 1.0) -> bytes:
    """生成音频数据（MP3格式）"""
    # 限制 rate 范围
    rate = max(0.5, min(2.0, rate))

    with tempfile.TemporaryDirectory() as tmpdir:
        # 分段处理
        segments = split_text(text)
        wav_files = []

        for i, seg in enumerate(segments):
            model_info = MODELS.get(seg['lang'], MODELS['zh'])
            wav_path = os.path.join(tmpdir, f'segment_{i}.wav')

            # 使用 --output_file 生成标准 WAV
            cmd = [
                PIPER_BIN,
                '--model', model_info['model'],
                '--config', model_info['config'],
                '--output_file', wav_path
            ]

            try:
                result = subprocess.run(
                    cmd,
                    input=seg['text'].encode('utf-8'),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=60
                )

                if result.returncode != 0:
                    raise Exception(f"Piper failed: {result.stderr.decode()}")

                if os.path.exists(wav_path):
                    wav_files.append(wav_path)
                else:
                    raise Exception(f"Piper did not create WAV file: {wav_path}")

            except subprocess.TimeoutExpired:
                raise Exception("TTS generation timeout")

        # 合并WAV文件
        if len(wav_files) == 1:
            combined_wav = wav_files[0]
        else:
            list_file = os.path.join(tmpdir, 'list.txt')
            with open(list_file, 'w') as f:
                for wav in wav_files:
                    f.write(f"file '{wav}'\n")

            combined_wav = os.path.join(tmpdir, 'combined.wav')
            subprocess.run([
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', list_file,
                combined_wav
            ], check=True)

        # 转换并调整语速
        mp3_path = os.path.join(tmpdir, 'output.mp3')

        # rate 转换：piper 输出是 22050Hz，用 atempo 调整速度
        # atempo 范围 0.5~2.0，直接用 rate 值
        subprocess.run([
            'ffmpeg', '-y', '-i', combined_wav,
            '-ar', '44100',
            '-ac', '2',
            '-b:a', '128k',
            '-filter:a', f'atempo={rate}',
            mp3_path
        ], check=True)

        # 读取MP3
        with open(mp3_path, 'rb') as f:
            return f.read()


@app.route('/')
def index():
    """返回静态网页"""
    return send_file(os.path.join(app.static_folder, 'index.html'))


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'engine': 'piper',
        'max_text_length': MAX_TEXT_LENGTH
    })


@app.route('/speak', methods=['POST'])
def speak():
    """文字转语音"""
    try:
        data = request.json or {}
        text = data.get('text', '')
        rate = float(data.get('rate', 1.0))

        if not text:
            return jsonify({'error': 'Text is required'}), 400

        if len(text) > MAX_TEXT_LENGTH:
            return jsonify({'error': f'Text too long (max {MAX_TEXT_LENGTH} chars)'}), 400

        # 限制 rate 范围
        rate = max(0.5, min(2.0, rate))

        # 生成音频
        audio_data = generate_audio(text, rate)

        if not audio_data:
            return jsonify({'error': 'Generation failed'}), 500

        # 返回音频（不作为附件，让前端可直接播放）
        return send_file(
            io.BytesIO(audio_data),
            mimetype='audio/mpeg'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("BrowserTTS v2 Server")
    print(f"Max text length: {MAX_TEXT_LENGTH}")
    print(f"Piper binary: {PIPER_BIN}")
    print("Engine: Piper TTS")
    print("Port: 5001")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5001, debug=False)