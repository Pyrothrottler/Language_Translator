# Language Translator - Capstone Project

An AI-powered language translation web application built with Flask and Google Translate API. This application provides real-time translation between 100+ languages with additional features like text-to-speech, language detection, and translation history.

## Features

- 🌐 **100+ Languages** - Support for over 100 languages worldwide
- ⚡ **Instant Translation** - Real-time AI-powered translation using Google Translate
- 🔍 **Auto Language Detection** - Automatically detects the source language
- 🔊 **Text to Speech** - Listen to translations with natural voice (gTTS)
- 🔄 **Language Swap** - Quickly swap source and target languages
- 📋 **Translation History** - Local storage of recent translations
- 📝 **Copy & Paste** - Easy clipboard integration
- ⌨️ **Keyboard Shortcuts** - Ctrl+Enter to translate, Ctrl+Shift+S to swap languages
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Modern UI** - Beautiful dark theme with glassmorphism design

## Tech Stack

- **Backend:** Python, Flask
- **Translation API:** googletrans (Google Translate API)
- **Text-to-Speech:** gTTS (Google Text-to-Speech)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Icons:** Font Awesome 6

## Project Structure

```
Language_Translator/
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── translator/
│   ├── __init__.py             # Module initialization
│   └── translation_service.py # Translation logic and supported languages
├── static/
│   ├── css/
│   │   └── style.css          # Application styles
│   └── js/
│       └── script.js          # Frontend logic
└── templates/
    └── index.html             # Main page template
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the project
```bash
cd Language_Translator
```

### Step 2: Create a virtual environment (recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the application
```bash
python app.py
```

### Step 5: Open in browser
Navigate to `http://localhost:5000` in your web browser.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/translate` | POST | Translate text |
| `/detect` | POST | Detect language |
| `/languages` | GET | Get supported languages |
| `/tts` | POST | Text-to-speech conversion |
| `/swap_languages` | POST | Swap source/target languages |

### Translate API Example

```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "source_lang": "auto", "target_lang": "fr"}'
```

## Usage Guide

1. **Enter Text:** Type or paste text in the source text area
2. **Select Languages:** Choose source language (or Auto Detect) and target language
3. **Translate:** Click the "Translate" button or press `Ctrl+Enter`
4. **Listen:** Click the speaker icons to hear the text spoken aloud
5. **Swap:** Click the swap button to exchange source and target languages
6. **History:** Click on any history item to reload a previous translation

## Keyboard Shortcuts

- `Ctrl + Enter` - Translate text
- `Ctrl + Shift + S` - Swap languages
- `Esc` - Clear text (when source textarea is focused)

## Troubleshooting

### googletrans issues
If you encounter issues with googletrans, try:
```bash
pip install --upgrade googletrans==4.0.0rc1
```

### Port already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## License

This project is created for educational purposes as a capstone project.

## Author

Created as a Capstone Project on Language Translation.