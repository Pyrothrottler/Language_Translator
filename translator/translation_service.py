import os
import tempfile
import requests
import json
from gtts import gTTS

# Supported languages dictionary: code -> language name
SUPPORTED_LANGUAGES = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'rw': 'Kinyarwanda',
    'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'tt': 'Tatar',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'tk': 'Turkmen',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'
}


class TranslationService:
    """Service class for handling language translation operations using LibreTranslate API."""

    def __init__(self):
        # Using the public LibreTranslate API (no API key needed)
        self.api_url = "https://libretranslate.com/translate"
        self.detect_url = "https://libretranslate.com/detect"
        self.languages_url = "https://libretranslate.com/languages"

    def translate_text(self, text, src_lang='auto', dest_lang='en'):
        """
        Translate text from source language to destination language.
        
        Args:
            text (str): The text to translate
            src_lang (str): Source language code (default: 'auto' for auto-detect)
            dest_lang (str): Destination language code (default: 'en')
        
        Returns:
            dict: Translation result with original text, translated text, 
                  source language, and detected language if auto
        """
        if not text or not text.strip():
            return {
                'success': False,
                'error': 'Please enter text to translate'
            }

        try:
            # For auto-detect, first detect the language
            detected_src = src_lang
            if src_lang == 'auto':
                detection = self.detect_language(text)
                if detection['success']:
                    detected_src = detection['language']
                else:
                    detected_src = 'en'

            # Make translation request
            payload = {
                'q': text,
                'source': detected_src,
                'target': dest_lang,
                'format': 'text'
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result.get('translatedText', '')
                
                return {
                    'success': True,
                    'original_text': text,
                    'translated_text': translated_text,
                    'source_language': detected_src,
                    'destination_language': dest_lang,
                    'source_language_name': SUPPORTED_LANGUAGES.get(detected_src, detected_src),
                    'destination_language_name': SUPPORTED_LANGUAGES.get(dest_lang, dest_lang),
                    'pronunciation': None
                }
            else:
                # Fallback: try Google Translate via googletrans
                return self._fallback_translate(text, src_lang, dest_lang)

        except Exception as e:
            # Fallback to googletrans if LibreTranslate fails
            return self._fallback_translate(text, src_lang, dest_lang)

    def _fallback_translate(self, text, src_lang='auto', dest_lang='en'):
        """Fallback translation using googletrans."""
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(text, src=src_lang, dest=dest_lang)
            
            return {
                'success': True,
                'original_text': text,
                'translated_text': result.text,
                'source_language': result.src,
                'destination_language': dest_lang,
                'source_language_name': SUPPORTED_LANGUAGES.get(result.src, result.src),
                'destination_language_name': SUPPORTED_LANGUAGES.get(dest_lang, dest_lang),
                'pronunciation': result.pronunciation if hasattr(result, 'pronunciation') else None
            }
        except Exception as e2:
            return {
                'success': False,
                'error': f'Translation failed: {str(e2)}'
            }

    def detect_language(self, text):
        """
        Detect the language of the given text.
        
        Args:
            text (str): The text to detect language for
        
        Returns:
            dict: Detection result with language code and confidence
        """
        if not text or not text.strip():
            return {
                'success': False,
                'error': 'Please enter text to detect language'
            }

        try:
            payload = {'q': text}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(self.detect_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                results = response.json()
                if results and len(results) > 0:
                    best = results[0]
                    return {
                        'success': True,
                        'language': best.get('language', 'en'),
                        'language_name': SUPPORTED_LANGUAGES.get(best.get('language', 'en'), 'English'),
                        'confidence': best.get('confidence', 0)
                    }
            
            # Fallback to googletrans
            return self._fallback_detect(text)

        except Exception as e:
            return self._fallback_detect(text)

    def _fallback_detect(self, text):
        """Fallback language detection using googletrans."""
        try:
            from googletrans import Translator
            translator = Translator()
            detection = translator.detect(text)
            return {
                'success': True,
                'language': detection.lang,
                'language_name': SUPPORTED_LANGUAGES.get(detection.lang, detection.lang),
                'confidence': detection.confidence
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Language detection failed: {str(e)}'
            }

    def text_to_speech(self, text, lang='en'):
        """
        Convert text to speech and save as an audio file.
        
        Args:
            text (str): The text to convert to speech
            lang (str): Language code for the speech (default: 'en')
        
        Returns:
            str: Path to the generated audio file, or None on failure
        """
        if not text or not text.strip():
            return None

        try:
            # Create a temporary file with .mp3 extension
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_path = temp_file.name
            temp_file.close()

            # Generate TTS
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_path)
            
            return temp_path

        except Exception as e:
            print(f"Text-to-speech failed: {str(e)}")
            return None

    def get_supported_languages(self):
        """Return the dictionary of supported languages."""
        return SUPPORTED_LANGUAGES