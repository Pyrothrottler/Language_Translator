// ===== DOM Elements =====
const sourceText = document.getElementById('sourceText');
const targetText = document.getElementById('targetText');
const sourceLang = document.getElementById('sourceLang');
const targetLang = document.getElementById('targetLang');
const translateBtn = document.getElementById('translateBtn');
const swapBtn = document.getElementById('swapBtn');
const clearBtn = document.getElementById('clearBtn');
const pasteBtn = document.getElementById('pasteBtn');
const copyBtn = document.getElementById('copyBtn');
const speakBtn = document.getElementById('speakBtn');
const speakSourceBtn = document.getElementById('speakSourceBtn');
const charCount = document.getElementById('charCount');
const detectedBadge = document.getElementById('detectedBadge');
const detectedLang = document.getElementById('detectedLang');
const historyList = document.getElementById('historyList');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');
const loadingOverlay = document.getElementById('loadingOverlay');

// ===== State =====
let translationHistory = JSON.parse(localStorage.getItem('translationHistory') || '[]');
let isTranslating = false;
let debounceTimer = null;

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    renderHistory();
    updateCharCount();
});

// ===== Character Count =====
sourceText.addEventListener('input', updateCharCount);

function updateCharCount() {
    const count = sourceText.value.length;
    charCount.textContent = count;
    charCount.style.color = count > 5000 ? '#ff6b81' : 'var(--text-muted)';
}

// ===== Auto-detect on input (debounced) =====
sourceText.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const text = sourceText.value.trim();
    
    if (text.length > 10 && sourceLang.value === 'auto') {
        debounceTimer = setTimeout(() => detectLanguage(text), 500);
    } else if (text.length <= 10) {
        detectedBadge.style.display = 'none';
    }
});

// ===== Language Detection =====
async function detectLanguage(text) {
    try {
        const response = await fetch('/detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        if (data.success) {
            detectedLang.textContent = data.language_name;
            detectedBadge.style.display = 'inline-flex';
        }
    } catch (error) {
        console.error('Language detection failed:', error);
    }
}

// ===== Translate =====
translateBtn.addEventListener('click', performTranslation);

// Ctrl+Enter shortcut
sourceText.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        performTranslation();
    }
});

async function performTranslation() {
    const text = sourceText.value.trim();
    
    if (!text) {
        showToast('Please enter text to translate', 'warning');
        sourceText.focus();
        return;
    }
    
    if (isTranslating) return;
    
    isTranslating = true;
    loadingOverlay.classList.add('active');
    
    try {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                source_lang: sourceLang.value,
                target_lang: targetLang.value
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            targetText.value = data.translated_text;
            
            // Update detected language badge
            if (sourceLang.value === 'auto' && data.source_language) {
                detectedLang.textContent = data.source_language_name;
                detectedBadge.style.display = 'inline-flex';
            }
            
            // Add to history
            addToHistory(text, data.translated_text, data.source_language_name, data.destination_language_name);
            
            // Animate the result
            targetText.style.animation = 'none';
            setTimeout(() => {
                targetText.style.animation = 'fadeIn 0.3s ease-out';
            }, 10);
        } else {
            showToast(data.error || 'Translation failed', 'error');
        }
    } catch (error) {
        showToast('Network error. Please try again.', 'error');
        console.error('Translation error:', error);
    } finally {
        isTranslating = false;
        loadingOverlay.classList.remove('active');
    }
}

// ===== Swap Languages =====
swapBtn.addEventListener('click', async () => {
    const currentSource = sourceLang.value;
    const currentTarget = targetLang.value;
    
    // Swap the text content
    const sourceTextValue = sourceText.value;
    const targetTextValue = targetText.value;
    
    sourceText.value = targetTextValue;
    targetText.value = '';
    updateCharCount();
    
    try {
        const response = await fetch('/swap_languages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                source_lang: currentSource,
                target_lang: currentTarget
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            sourceLang.value = data.source_lang;
            targetLang.value = data.target_lang;
            
            // Hide detected badge if source is auto
            if (data.source_lang === 'auto') {
                detectedBadge.style.display = 'none';
            }
        }
    } catch (error) {
        console.error('Swap failed:', error);
    }
    
    // Auto-translate if there's text
    if (sourceText.value.trim()) {
        performTranslation();
    }
});

// ===== Clear Text =====
clearBtn.addEventListener('click', () => {
    sourceText.value = '';
    targetText.value = '';
    updateCharCount();
    detectedBadge.style.display = 'none';
    sourceText.focus();
});

// ===== Paste =====
pasteBtn.addEventListener('click', async () => {
    try {
        const text = await navigator.clipboard.readText();
        sourceText.value = text;
        updateCharCount();
        showToast('Text pasted from clipboard', 'success');
    } catch (error) {
        showToast('Unable to paste. Allow clipboard access.', 'warning');
    }
});

// ===== Copy Translation =====
copyBtn.addEventListener('click', async () => {
    const text = targetText.value;
    
    if (!text) {
        showToast('Nothing to copy', 'warning');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
    } catch (error) {
        showToast('Copy failed', 'error');
    }
});

// ===== Text to Speech =====
speakBtn.addEventListener('click', () => {
    const text = targetText.value;
    if (!text) {
        showToast('Nothing to speak', 'warning');
        return;
    }
    speakText(text, targetLang.value);
});

speakSourceBtn.addEventListener('click', () => {
    const text = sourceText.value;
    if (!text) {
        showToast('Nothing to speak', 'warning');
        return;
    }
    const lang = sourceLang.value === 'auto' ? 'en' : sourceLang.value;
    speakText(text, lang);
});

async function speakText(text, lang) {
    try {
        const response = await fetch('/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, lang })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const audio = new Audio(url);
            audio.play();
            audio.onended = () => URL.revokeObjectURL(url);
        } else {
            showToast('Text-to-speech failed', 'error');
        }
    } catch (error) {
        showToast('Speech generation failed', 'error');
    }
}

// ===== Translation History =====
function addToHistory(original, translated, sourceName, targetName) {
    const entry = {
        id: Date.now(),
        original,
        translated,
        sourceName,
        targetName,
        timestamp: new Date().toLocaleString()
    };
    
    translationHistory.unshift(entry);
    
    // Keep only last 50 entries
    if (translationHistory.length > 50) {
        translationHistory = translationHistory.slice(0, 50);
    }
    
    localStorage.setItem('translationHistory', JSON.stringify(translationHistory));
    renderHistory();
}

function renderHistory() {
    if (translationHistory.length === 0) {
        historyList.innerHTML = `
            <div class="empty-history">
                <i class="fas fa-book-open"></i>
                <p>No translations yet. Start translating!</p>
            </div>
        `;
        return;
    }
    
    historyList.innerHTML = translationHistory.map(entry => `
        <div class="history-item" onclick="loadFromHistory(${entry.id})">
            <div class="history-content">
                <span class="lang-badge">${entry.sourceName} → ${entry.targetName}</span>
                <div class="original">${escapeHtml(entry.original)}</div>
                <div class="translated">${escapeHtml(entry.translated)}</div>
            </div>
            <span class="time">${entry.timestamp}</span>
        </div>
    `).join('');
}

function loadFromHistory(id) {
    const entry = translationHistory.find(e => e.id === id);
    if (entry) {
        sourceText.value = entry.original;
        targetText.value = entry.translated;
        updateCharCount();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

clearHistoryBtn.addEventListener('click', () => {
    if (translationHistory.length === 0) {
        showToast('History is already empty', 'warning');
        return;
    }
    
    translationHistory = [];
    localStorage.removeItem('translationHistory');
    renderHistory();
    showToast('History cleared', 'success');
});

// ===== Utility Functions =====
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(message, type = 'success') {
    toastMessage.textContent = message;
    
    const icon = toast.querySelector('.toast-content i');
    icon.className = type === 'success' ? 'fas fa-check-circle' : 
                     type === 'warning' ? 'fas fa-exclamation-circle' : 
                     'fas fa-times-circle';
    icon.style.color = type === 'success' ? '#2ecc71' : 
                       type === 'warning' ? '#f39c12' : 
                       '#e74c3c';
    
    toast.classList.add('show');
    
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ===== Keyboard Shortcuts =====
document.addEventListener('keydown', (e) => {
    // Ctrl+Shift+S: Swap languages
    if (e.ctrlKey && e.shiftKey && e.key === 'S') {
        e.preventDefault();
        swapBtn.click();
    }
    
    // Escape: Clear text
    if (e.key === 'Escape' && document.activeElement === sourceText) {
        if (sourceText.value) {
            clearBtn.click();
        }
    }
});

// ===== Auto-resize textarea =====
sourceText.addEventListener('input', autoResize);
targetText.addEventListener('input', autoResize);

function autoResize() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 300) + 'px';
}