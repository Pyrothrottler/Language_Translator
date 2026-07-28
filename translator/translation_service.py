import os
import tempfile
import time
import random
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
    """Service class for handling language translation operations using MyMemory API."""
    
    # Mymemory language code mapping (similar to Google's but may differ)
    LANG_MAP = {
        'zh-cn': 'zh-CN',
        'zh-tw': 'zh-TW',
        'iw': 'he',
        'jw': 'jv',
    }

    def __init__(self):
        self.translate_url = "https://api.mymemory.translated.net/get"
        self.detect_url = "https://api.mymemory.translated.net/language/detect"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }

    def _map_lang(self, lang_code):
        """Map language codes for MyMemory API compatibility."""
        return self.LANG_MAP.get(lang_code, lang_code)

    def translate_text(self, text, src_lang='auto', dest_lang='en'):
        """
        Translate text using MyMemory API (or Lingva fallback for auto-detection).
        """
        if not text or not text.strip():
            return {'success': False, 'error': 'Please enter text to translate'}

        # MyMemory doesn't support 'auto' as source - use Lingva which does
        if src_lang == 'auto':
            return self._translate_via_lingva(text, src_lang, dest_lang)

        try:
            params = {
                'q': text,
                'langpair': f'{self._map_lang(src_lang)}|{self._map_lang(dest_lang)}',
                'de': 'translator@example.com'
            }
            
            response = requests.get(self.translate_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('responseStatus') == 200:
                    translated_text = data.get('responseData', {}).get('translatedText', '')
                    detected_src = data.get('responseData', {}).get('detectedLanguage', src_lang)
                    
                    if not detected_src or detected_src == 'und':
                        detected_src = src_lang
                    
                    if translated_text and translated_text.lower() != text.lower():
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
                        return self._translate_via_lingva(text, src_lang, dest_lang)
                else:
                    error_msg = data.get('responseDetails', '')
                    if '403' in error_msg or 'LIMIT' in error_msg.upper():
                        return self._translate_via_lingva(text, src_lang, dest_lang)
                    return {'success': False, 'error': f'Translation failed: {error_msg}'}
            elif response.status_code == 429:
                return self._translate_via_lingva(text, src_lang, dest_lang)
            else:
                return self._translate_via_lingva(text, src_lang, dest_lang)

        except requests.exceptions.Timeout:
            return self._translate_via_lingva(text, src_lang, dest_lang)
        except requests.exceptions.ConnectionError:
            return {'success': False, 'error': 'Could not connect to translation service.'}
        except Exception as e:
            return self._translate_via_lingva(text, src_lang, dest_lang)

    def _translate_via_lingva(self, text, src_lang='auto', dest_lang='en'):
        """Fallback translation using Lingva (a free Google Translate frontend)."""
        try:
            # Using multiple Lingva instances for redundancy
            instances = [
                f"https://lingva.ml/api/v1/{src_lang}/{dest_lang}/{requests.utils.quote(text)}",
                f"https://lingva.gabmus.org/api/v1/{src_lang}/{dest_lang}/{requests.utils.quote(text)}",
            ]
            
            for url in instances:
                try:
                    r = requests.get(url, timeout=8)
                    if r.status_code == 200:
                        data = r.json()
                        translated = data.get('translation', '')
                        detected = data.get('info', {}).get('detectedSource', src_lang)
                        if translated and translated.lower() != text.lower():
                            return {
                                'success': True,
                                'original_text': text,
                                'translated_text': translated,
                                'source_language': detected,
                                'destination_language': dest_lang,
                                'source_language_name': SUPPORTED_LANGUAGES.get(detected, detected),
                                'destination_language_name': SUPPORTED_LANGUAGES.get(dest_lang, dest_lang),
                                'pronunciation': None
                            }
                except Exception:
                    continue
            
            return {'success': False, 'error': 'All translation services are currently unavailable. Please try again later.'}
            
        except Exception as e:
            return {'success': False, 'error': f'Translation failed: {str(e)}'}

    def detect_language(self, text):
        """Detect language using MyMemory API."""
        if not text or not text.strip():
            return {'success': False, 'error': 'Please enter text to detect language'}

        try:
            # Try detecting via MyMemory translation endpoint first
            params = {
                'q': text[:50],  # Short sample is enough for detection
                'langpair': 'auto|en',
                'de': 'translator@example.com'
            }
            
            response = requests.get(self.translate_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                detected = data.get('responseData', {}).get('detectedLanguage', '')
                if detected and detected != 'und':
                    return {
                        'success': True,
                        'language': detected,
                        'language_name': SUPPORTED_LANGUAGES.get(detected, detected),
                        'confidence': 0.8
                    }
            
            # Fallback: try Lingva detection
            try:
                encoded = requests.utils.quote(text[:50])
                r = requests.get(f"https://lingva.ml/api/v1/auto/en/{encoded}", timeout=8)
                if r.status_code == 200:
                    data = r.json()
                    detected = data.get('info', {}).get('detectedSource', '')
                    if detected:
                        return {
                            'success': True,
                            'language': detected,
                            'language_name': SUPPORTED_LANGUAGES.get(detected, detected),
                            'confidence': 0.7
                        }
            except Exception:
                pass
            
            return {'success': False, 'error': 'Could not detect language from text'}

        except Exception as e:
            return {'success': False, 'error': f'Language detection failed: {str(e)}'}

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