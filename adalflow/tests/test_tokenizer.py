import unittest
from adalflow.core.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):

    def test_tokenizer_initialization(self):
        tokenizer = Tokenizer()
        self.assertEqual(tokenizer.name, "cl100k_base")
        self.assertIsNotNone(tokenizer.tokenizer)

    def test_encode_decode(self):
        tokenizer = Tokenizer()
        text = "Hello, world! This is a test."
        encoded = tokenizer.encode(text)
        self.assertIsInstance(encoded, list)
        self.assertTrue(len(encoded) > 0)

        decoded = tokenizer.decode(encoded)
        self.assertEqual(decoded, text)

    def test_get_string_tokens_ascii(self):
        tokenizer = Tokenizer()
        text = "Hello, world! This is a test."

        # Test our optimized method
        tokens = tokenizer.get_string_tokens(text)

        # Manually compute using standard fallback way
        expected_tokens = [tokenizer.tokenizer.decode([t]) for t in tokenizer.encode(text)]

        self.assertEqual(tokens, expected_tokens)

    def test_get_string_tokens_unicode(self):
        tokenizer = Tokenizer()
        text = "你好，世界！🌟 Unicode test."

        tokens = tokenizer.get_string_tokens(text)
        expected_tokens = [tokenizer.tokenizer.decode([t]) for t in tokenizer.encode(text)]

        self.assertEqual(tokens, expected_tokens)

    def test_fallback_behavior(self):
        tokenizer = Tokenizer()
        original_encoder = tokenizer.tokenizer

        # Create a mock tokenizer that delegates to the original but doesn't have decode_single_token_bytes
        class MockEncoder:
            def __init__(self, original):
                self._original = original

            def encode(self, text):
                return self._original.encode(text)

            def decode(self, tokens):
                return self._original.decode(tokens)

        tokenizer.tokenizer = MockEncoder(original_encoder)

        text = "Hello world! 你好 🌟"
        tokens = tokenizer.get_string_tokens(text)

        # The fallback should use standard decode
        expected_tokens = [tokenizer.tokenizer.decode([t]) for t in tokenizer.encode(text)]
        self.assertEqual(tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()
