import os
import uuid
from flask import Flask, render_template, request, jsonify, send_file
from translator import TranslationService, SUPPORTED_LANGUAGES

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize translation service
translation_service = TranslationService()

# Store temporary audio files for cleanup
_temp_files = set()


@app.route('/')
def index():
    """Render the main page with supported languages."""
    return render_template(
        'index.html',
        languages=SUPPORTED_LANGUAGES
    )


@app.route('/translate', methods=['POST'])
def translate():
    """
    API endpoint to translate text.
    
    Expects JSON: { "text": "...", "source_lang": "auto", "target_lang": "en" }
    Returns JSON with translation result.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    text = data.get('text', '')
    source_lang = data.get('source_lang', 'auto')
    target_lang = data.get('target_lang', 'en')
    
    result = translation_service.translate_text(text, source_lang, target_lang)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@app.route('/detect', methods=['POST'])
def detect():
    """
    API endpoint to detect language of text.
    
    Expects JSON: { "text": "..." }
    Returns JSON with detection result.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    text = data.get('text', '')
    result = translation_service.detect_language(text)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@app.route('/languages', methods=['GET'])
def get_languages():
    """API endpoint to get all supported languages."""
    return jsonify({
        'success': True,
        'languages': SUPPORTED_LANGUAGES
    })


@app.route('/tts', methods=['POST'])
def text_to_speech():
    """
    API endpoint to convert text to speech.
    
    Expects JSON: { "text": "...", "lang": "en" }
    Returns audio file.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    text = data.get('text', '')
    lang = data.get('lang', 'en')
    
    audio_path = translation_service.text_to_speech(text, lang)
    
    if audio_path:
        _temp_files.add(audio_path)
        return send_file(
            audio_path,
            mimetype='audio/mpeg',
            as_attachment=False
        )
    else:
        return jsonify({'success': False, 'error': 'Text-to-speech conversion failed'}), 500


@app.route('/swap_languages', methods=['POST'])
def swap_languages():
    """
    API endpoint to swap source and target languages.
    
    Expects JSON: { "source_lang": "en", "target_lang": "fr" }
    Returns JSON with swapped languages.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    source_lang = data.get('source_lang', 'auto')
    target_lang = data.get('target_lang', 'en')
    
    # Swap the languages
    new_source = target_lang
    new_target = source_lang if source_lang != 'auto' else 'en'
    
    return jsonify({
        'success': True,
        'source_lang': new_source,
        'target_lang': new_target,
        'source_lang_name': SUPPORTED_LANGUAGES.get(new_source, 'Auto Detect'),
        'target_lang_name': SUPPORTED_LANGUAGES.get(new_target, new_target)
    })


@app.teardown_request
def cleanup_temp_files(exception=None):
    """Clean up temporary audio files after request."""
    for file_path in list(_temp_files):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            _temp_files.discard(file_path)
        except Exception:
            pass


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)