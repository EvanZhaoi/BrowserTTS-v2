// BrowserTTS v2 - Background Script

// 创建右键菜单
chrome.contextMenus.create({
  id: 'tts-save',
  title: '保存为音频 🎵',
  contexts: ['selection']
});

// 监听右键菜单点击
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'tts-save' && info.selectionText) {
    chrome.tabs.sendMessage(tab.id, {
      action: 'generate',
      text: info.selectionText
    });
  }
});

console.log('BrowserTTS v2 loaded');
