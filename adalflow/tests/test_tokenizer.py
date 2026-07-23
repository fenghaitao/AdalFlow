import unittest
import pytest
from adalflow.core.tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):
    def test_default_tokenizer_initialization(self):
        tokenizer = Tokenizer()
        self.assertEqual(tokenizer.name, "cl100k_base")
        self.assertEqual(tokenizer.stop_words, set())

    def test_tokenizer_initialization_with_stop_words(self):
        tokenizer = Tokenizer(remove_stop_words=True)
        self.assertIn("the", tokenizer.stop_words)
        self.assertIn("and", tokenizer.stop_words)

    def test_encode_decode(self):
        tokenizer = Tokenizer()
        text = "Hello, world!"
        token_ids = tokenizer.encode(text)
        self.assertIsInstance(token_ids, list)
        self.assertTrue(len(token_ids) > 0)

        decoded_text = tokenizer.decode(token_ids)
        self.assertEqual(decoded_text, text)

    def test_count_tokens(self):
        tokenizer = Tokenizer()
        text = "Hello, world!"
        count = tokenizer.count_tokens(text)
        self.assertEqual(count, len(tokenizer.encode(text)))

    def test_get_string_tokens_ascii(self):
        tokenizer = Tokenizer()
        text = "Hello world"
        string_tokens = tokenizer.get_string_tokens(text)
        self.assertIsInstance(string_tokens, list)
        # Reconstructing text from string tokens (in tiktoken space) should equal original text
        reconstructed = "".join(string_tokens)
        self.assertEqual(reconstructed, text)

    def test_get_string_tokens_unicode_and_emojis(self):
        tokenizer = Tokenizer()
        text = "Hello, 世界! 🚀"
        string_tokens = tokenizer.get_string_tokens(text)
        self.assertIsInstance(string_tokens, list)
        reconstructed = "".join(string_tokens)
        # Reconstructing from individual token string pieces where multi-byte UTF-8
        # characters are split across tokens yields placeholder replacement characters (\uFFFD),
        # which is the correct and expected behavior for both old and new implementations.
        self.assertEqual(reconstructed, "Hello, \uFFFD\uFFFD\u754C! \uFFFD\uFFFD\uFFFD")

    def test_get_string_tokens_empty(self):
        tokenizer = Tokenizer()
        string_tokens = tokenizer.get_string_tokens("")
        self.assertEqual(string_tokens, [])

if __name__ == "__main__":
    pytest.main()
