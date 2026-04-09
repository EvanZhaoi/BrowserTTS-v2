<template>
  <div class="container">
    <h1>BrowserTTS 网页工具</h1>
    
    <div class="text-input">
      <textarea 
        v-model="text" 
        placeholder="请输入要转换的文字..."
        rows="6"
      ></textarea>
    </div>
    
    <div class="slider-container">
      <label>语速：{{ rate.toFixed(1) }}x</label>
      <input 
        type="range" 
        v-model.number="rate" 
        min="0.5" 
        max="2.0" 
        step="0.1"
      >
      <div class="slider-labels">
        <span>慢速</span>
        <span>正常</span>
        <span>快速</span>
      </div>
    </div>
    
    <div class="btn-container">
      <button 
        @click="generateAudio" 
        :disabled="!text || loading"
        class="btn-download"
      >
        {{ loading ? '生成中...' : '生成并下载 MP3' }}
      </button>
    </div>
    
    <div class="status" :class="statusClass">
      {{ status }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const text = ref('')
const rate = ref(1.0)
const loading = ref(false)
const status = ref('')
const statusType = ref<'success' | 'error' | ''>('')

const statusClass = computed(() => {
  if (statusType.value === 'success') return 'status-success'
  if (statusType.value === 'error') return 'status-error'
  return ''
})

async function generateAudio() {
  if (!text.value || loading.value) return
  
  loading.value = true
  status.value = '正在生成音频...'
  statusType.value = ''
  
  try {
    const response = await fetch('http://localhost:5001/speak', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text.value,
        rate: rate.value
      })
    })
    
    if (!response.ok) {
      throw new Error('请求失败')
    }
    
    const blob = await response.blob()
    
    // 下载文件
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'tts_' + Date.now() + '.mp3'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    status.value = '✅ 下载成功！'
    statusType.value = 'success'
    
  } catch (err: any) {
    status.value = '❌ ' + (err.message || '生成失败')
    statusType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f7;
  min-height: 100vh;
  padding: 20px;
}

.container {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

h1 {
  text-align: center;
  color: #1d1d1f;
  margin-bottom: 30px;
  font-size: 24px;
}

.text-input textarea {
  width: 100%;
  padding: 15px;
  border: 2px solid #e5e5e7;
  border-radius: 12px;
  font-size: 16px;
  resize: vertical;
  transition: border-color 0.2s;
}

.text-input textarea:focus {
  outline: none;
  border-color: #007AFF;
}

.slider-container {
  margin: 25px 0;
}

.slider-container label {
  display: block;
  margin-bottom: 10px;
  color: #1d1d1f;
  font-weight: 500;
}

.slider-container input[type="range"] {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: #e5e5e7;
  -webkit-appearance: none;
}

.slider-container input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #007AFF;
  cursor: pointer;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  color: #86868b;
}

.btn-download {
  width: 100%;
  padding: 16px;
  background: #007AFF;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-download:hover:not(:disabled) {
  background: #0056b3;
}

.btn-download:disabled {
  background: #c7c7cc;
  cursor: not-allowed;
}

.status {
  text-align: center;
  margin-top: 20px;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
}

.status-success {
  background: #d4edda;
  color: #155724;
}

.status-error {
  background: #f8d7da;
  color: #721c24;
}
</style>
