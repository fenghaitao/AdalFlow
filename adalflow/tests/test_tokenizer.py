import unittest
from adalflow.core.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_get_string_tokens_ascii(self):
        text = "Hello, world! This is a simple test."
        tokens = self.tokenizer.get_string_tokens(text)
        expected = [self.tokenizer.tokenizer.decode([tid]) for tid in self.tokenizer.encode(text)]
        self.assertEqual(tokens, expected)

    def test_get_string_tokens_unicode(self):
        text = "你好，这是一个用于测试的分词器。Hello, world!"
        tokens = self.tokenizer.get_string_tokens(text)
        expected = [self.tokenizer.tokenizer.decode([tid]) for tid in self.tokenizer.encode(text)]
        self.assertEqual(tokens, expected)

    def test_count_tokens(self):
        text = "Hello, world!"
        self.assertEqual(self.tokenizer.count_tokens(text), 4)


if __name__ == "__main__":
    unittest.main()
