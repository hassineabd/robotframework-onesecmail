
import unittest
from OneSecMail.keywords._languagedetector import _LanguageDetector, LanguageCode

class TestLanguageDetector(unittest.TestCase):

    def setUp(self):
        """Set up the LanguageDetector instance for testing."""
        self.detector = _LanguageDetector()

    def test_detect_language_valid(self):
        """Test language detection for valid input."""
        text = "Bonjour, comment ça va?"  # French text
        detected_language = self.detector.detect_language(text)
        self.assertEqual(detected_language, LanguageCode.FR.value)

    def test_detect_language_invalid(self):
        """Test language detection for invalid input."""
        text = ""  # Empty text
        detected_language = self.detector.detect_language(text)
        self.assertEqual(detected_language, self.detector.default_language)

    def test_assert_language_is_valid(self):
        """Test assertion for expected language."""
        text = "Hello, how are you?"  # English text
        try:
            self.detector.assert_language_is(text, 'english')
        except AssertionError:
            self.fail("assert_language_is raised AssertionError unexpectedly!")

    def test_assert_language_is_invalid(self):
        """Test assertion for unsupported expected language."""
        text = "Hola, ¿cómo estás?"  # Spanish text
        with self.assertRaises(SystemError):
            self.detector.assert_language_is(text, 'unsupported_language')

    def test_assert_language_is_mismatch(self):
        """Test assertion for language mismatch."""
        text = "Bonjour, comment ça va?"  # French text
        with self.assertRaises(AssertionError):
            self.detector.assert_language_is(text, 'english')

if __name__ == '__main__':
    unittest.main()