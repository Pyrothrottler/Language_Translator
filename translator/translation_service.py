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
    """Service class for handling language translation operations using Google Translate API."""

    def __init__(self):
        # Google Translate API endpoints (same ones googletrans uses internally)
        self.translate_url = "https://translate.googleapis.com/translate_a/single"
        self.detect_url = "https://translate.googleapis.com/translate_a/detect"

    def _normalize_lang_code(self, lang_code):
        """Normalize language codes for Google Translate API compatibility."""
        # Map common codes that differ between our list and Google's
        mapping = {
            'zh-cn': 'zh-CN',
            'zh-tw': 'zh-TW',
            'iw': 'iw',  # Hebrew
            'jw': 'jw',  # Javanese
        }
        return mapping.get(lang_code, lang_code)

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
            params = {
                'client': 'gtx',
                'sl': self._normalize_lang_code(src_lang),
                'tl': self._normalize_lang_code(dest_lang),
                'dt': 't',
                'q': text
            }
            
            response = requests.get(self.translate_url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                # Parse Google Translate response format
                translated_text = ''
                if result and len(result) > 0 and result[0]:
                    for sentence in result[0]:
                        if sentence and len(sentence) > 0 and sentence[0]:
                            translated_text += sentence[0]
                
                # Detect language from response when auto is used
                detected_src = src_lang
                if src_lang == 'auto' and result and len(result) > 2 and result[2]:
                    detected_src = result[2]
                
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
                return {
                    'success': False,
                    'error': f'Translation service returned status {response.status_code}'
                }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Translation request timed out. Please try again.'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Could not connect to translation service. Check your internet connection.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Translation failed: {str(e)}'
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
            params = {
                'client': 'gtx',
                'sl': 'auto',
                'tl': 'en',
                'dt': 't',
                'q': text
            }
            
            response = requests.get(self.translate_url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 2 and result[2]:
                    detected_lang = result[2]
                    confidence = 1.0
                    return {
                        'success': True,
                        'language': detected_lang,
                        'language_name': SUPPORTED_LANGUAGES.get(detected_lang, detected_lang),
                        'confidence': confidence
                    }
            
            return {
                'success': False,
                'error': 'Could not detect language from text'
            }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Detection request timed out. Please try again.'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Could not connect to detection service. Check your internet connection.'
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