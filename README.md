# 🌐 Language Translator - Capstone Project

> **⚠️ IMPORTANT: GitHub only shows this README file (documentation). To use the actual translator app, you must run it locally or deploy it (see instructions below).**

An AI-powered language translation web application built with Flask. This application provides real-time translation between 100+ languages with additional features like text-to-speech, language detection, and translation history.

## Features

- 🌐 **100+ Languages** - Support for over 100 languages worldwide
- ⚡ **Instant Translation** - Real-time AI-powered translation
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
- **Translation API:** LibreTranslate + Google Translate (fallback)
- **Text-to-Speech:** gTTS (Google Text-to-Speech)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Icons:** Font Awesome 6

## Project Structure

```
Language_Translator/
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
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

## 🚀 How to Actually Run the App (See the UI)

### Option 1: Run Locally (On Your Computer)

#### Prerequisites
- Python 3.8 or higher installed on your computer
- pip (Python package manager - comes with Python)

#### Step-by-step:

**Step 1:** Open terminal/command prompt and navigate to the project folder:
```bash
cd Language_Translator
```

**Step 2:** Create a virtual environment (recommended to avoid conflicts):
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

**Step 3:** Install the required packages:
```bash
pip install -r requirements.txt
```

**Step 4:** Start the application server:
```bash
python app.py
```

**Step 5:** Open your web browser and go to:
```
http://localhost:5000
```

**That's it!** The translator UI will appear in your browser with input boxes, language selectors, and a translate button.

---

### Option 2: Deploy on Render (Free - So Anyone Can Use It Online)

> **Follow these steps EXACTLY:**

#### Step 1: Push your code to GitHub first
```bash
# In your project folder, run:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

#### Step 2: Go to Render and create an account
1. Open your browser and go to: **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up using **GitHub** (easiest - click "Continue with GitHub")
4. Complete the signup process

#### Step 3: Create a new Web Service
1. Once logged in, click the **"New +"** button (top right)
2. Select **"Web Service"** from the dropdown

#### Step 4: Connect your GitHub repository
1. Click **"Connect a repository"** or **"Connect account"** if not connected
2. Find and select your repository (the one you pushed to GitHub)
3. Click **"Connect"**

#### Step 5: Configure the service
Fill in these EXACT values:

| Field | Value |
|-------|-------|
| **Name** | `language-translator` (or any name you want) |
| **Region** | Choose the one closest to you (e.g., `Frankfurt`) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | **Free** (scroll down to select it) |

#### Step 6: Deploy
1. Scroll down and click **"Create Web Service"**
2. Wait 2-5 minutes while Render builds and deploys your app
3. Once done, you'll see a URL like: `https://language-translator.onrender.com`
4. **Click that URL** - your translator app is now live!

> **⚠️ Note:** The free Render plan puts the app to sleep after 15 minutes of inactivity. The first visit after sleep may take 30-60 seconds to wake up. This is normal.

---

## 📖 Usage Guide (Once the app is running)

1. **Enter Text:** Type or paste text in the source text area
2. **Select Languages:** Choose source language (or Auto Detect) and target language
3. **Translate:** Click the "Translate" button or press `Ctrl+Enter`
4. **Listen:** Click the speaker icons to hear the text spoken aloud
5. **Swap:** Click the swap button to exchange source and target languages
6. **History:** Click on any history item to reload a previous translation

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

### Render deployment fails
- Make sure you have a `Procfile` file with exactly: `web: gunicorn app:app`
- Make sure `gunicorn` is in your `requirements.txt`
- Check the build logs on Render for specific errors

## License

This project is created for educational purposes as a capstone project.

## Author

Created as a Capstone Project on Language Translation.