from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from robot.api import logger
from robot.api.deco import keyword, not_keyword
from enum import Enum
from .keywordgroup import KeywordGroup

"""
Language detection methods using : https://github.com/shuyo/language-detection/tree/master/lib
package : https://pypi.org/project/langdetect/
"""
class LanguageCode(Enum):
    FR = 'fr'  # French
    EN = 'en'  # English
    ES = 'es'  # Spanish
    DE = 'de'  # German
    IT = 'it'  # Italian
    PT = 'pt'  # Portuguese
    NL = 'nl'  # Dutch
    RU = 'ru'  # Russian
    ZH = 'zh'  # Chinese
    JA = 'ja'  # Japanese
    AR = 'ar'  # Arabic

#refer to doc the check the rest of lanugage
    _language_mapping = {
        'french': FR,
        'english': EN,
        'spanish': ES,
        'german': DE,
        'italian': IT,
        'portuguese': PT,
        'dutch': NL,
        'russian': RU,
        'chinese': ZH,
        'japanese': JA,
        'arabic': AR
    }


    @classmethod
    def from_language_name(cls, language_name):
        return cls._language_mapping.value.get(language_name.lower())
    
    @classmethod
    def from_language_code(cls, language_code):
        reverse_mapping = {v.value: k for k, v in cls._language_mapping}
        return reverse_mapping.get(language_code)

    # @classmethod
    # def from_language_name(cls, language_name):
    #     language_mapping = {
    #         'french': cls.FR,
    #         'english': cls.EN,
    #         'spanish': cls.ES,
    #         'german': cls.DE,
    #         'italian': cls.IT,
    #         'portuguese': cls.PT,
    #         'dutch': cls.NL,
    #         'russian': cls.RU,
    #         'chinese': cls.ZH,
    #         'japanese': cls.JA,
    #         'arabic': cls.AR
    #     }
    #     return language_mapping.get(language_name.lower())
    
    @classmethod
    def from_language_code(cls, language_code):
        member = cls._language_mapping.get(language_code)
        logger.info(f"member : {member}.")
        logger.info(f"member.name : {member.name}.")
        logger.info(f"member.value : {member.value}.")
        return member.name.lower() if member else None

class _LanguageDetector(KeywordGroup):
    DetectorFactory.seed = 0
    default_language = 'unknown'
    
    #private method
    def __detect_language(self, text):
        try:
            language = detect(text)
            return language
        except LangDetectException:
            return self.default_language
        

    def __assert_language_is(self, text, expected_language_name):
        """Private method to check if language matches expected language.
        
        Args:
            text (str): Text to check language of
            expected_language_name (str): Expected language name
            
        Returns:
            tuple: Contains expected_enum, detected_enum for validation
        """
        expected_enum = LanguageCode.from_language_name(expected_language_name)
        detected_enum = self.__detect_language(text)
        return expected_enum, detected_enum

    @keyword 
    def assert_language_is(self, text, expected_language_name):
        """Assert that text is in the expected language.
        
        Args:
            text (str): Text to check language of
            expected_language_name (str): Expected language name
            
        Raises:
            SystemError: If expected language is not supported
            AssertionError: If detected language does not match expected
        """        
        expected_enum, detected_enum = self.__assert_language_is(text, expected_language_name)
        if expected_enum is None:
            raise SystemError(f"Language '{expected_language_name}' is not supported. Please use a valid language name.")
        
        if detected_enum != expected_enum:
            detected_name = LanguageCode.from_language_code(detected_enum.upper())
            raise AssertionError(f"Language mismatch: expected {expected_language_name}, got {detected_name}")


    @keyword
    def detect_language(self, text):
        """Detect the language of the given text.
        
        Args:
            text (str): The text to detect the language for
            
        Returns:
            str: The detected language code
            
        Raises:
            ValueError: If the language cannot be detected or is not supported
        """
        if not text or not text.strip():
            raise ValueError (f"Argument 'text' is empty or not text. Please provide valid text.") 
            
        detected_language = self.__detect_language(text)
        if detected_language == self.default_language:
            raise ValueError (f"Unable to detect language. Please provide valid text.")
        self._info(f"Detected language: {detected_language}")
        return detected_language
