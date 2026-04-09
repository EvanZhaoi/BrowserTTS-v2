// BrowserTTS v2 - Content Script

// 监听来自后台的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'generate') {
    generateAudio(message.text);
  }
});

async function generateAudio(text) {
  showToast('正在生成音频...', 'loading');
  
  try {
    const response = await fetch('http://localhost:5001/speak', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        rate: 1.0
      })
    });
    
    if (!response.ok) {
      throw new Error('请求失败: ' + response.status);
    }
    
    const blob = await response.blob();
    
    // 创建下载
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'tts_' + Date.now() + '.mp3';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast('✅ 下载成功！', 'success');
    
  } catch (err) {
    console.error('TTS Error:', err);
    showToast('❌ ' + err.message, 'error');
  }
}

function showToast(message, type) {
  const existing = document.getElementById('tts-toast');
  if (existing) existing.remove();
  
  const toast = document.createElement('div');
  toast.id = 'tts-toast';
  toast.textContent = message;
  
  const colors = {
    loading: '#007AFF',
    success: '#34C759',
    error: '#FF3B30'
  };
  
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 999999;
    padding: 12px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    background: ${colors[type] || '#007AFF'};
    color: white;
    transition: opacity 0.3s;
  `;
  
  document.body.appendChild(toast);
  
  // 3秒后自动消失
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

console.log('BrowserTTS v2 content script loaded');
