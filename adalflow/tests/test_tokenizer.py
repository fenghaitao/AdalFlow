import tiktoken

from adalflow.core.tokenizer import Tokenizer


def test_tokenizer_initialization():
    tokenizer = Tokenizer()
    assert tokenizer.name == "cl100k_base"
    assert tokenizer.stop_words == set()

    tokenizer_stop = Tokenizer(remove_stop_words=True)
    assert "the" in tokenizer_stop.stop_words

def test_tokenizer_encode_decode():
    tokenizer = Tokenizer()
    text = "Hello, world! This is AdalFlow."
    token_ids = tokenizer.encode(text)
    assert isinstance(token_ids, list)
    assert len(token_ids) > 0
    assert all(isinstance(tid, int) for tid in token_ids)

    decoded = tokenizer.decode(token_ids)
    assert decoded == text

def test_tokenizer_count_tokens():
    tokenizer = Tokenizer()
    text = "Hello, world!"
    assert tokenizer.count_tokens(text) == len(tokenizer.encode(text))

def test_tokenizer_get_string_tokens():
    tokenizer = Tokenizer()
    text = "Hello, world! 🌍 Beautiful Day."
    string_tokens = tokenizer.get_string_tokens(text)
    assert isinstance(string_tokens, list)
    assert len(string_tokens) > 0
    assert all(isinstance(t, str) for t in string_tokens)

    # Reconstructing the string from string tokens will contain replacement characters for split multi-byte characters,
    # which is exactly consistent with the original tiktoken behavior of decoding split tokens individually.
    reconstructed = "".join(string_tokens)

    enc = tiktoken.get_encoding("cl100k_base")
    expected = "".join([enc.decode([tid]) for tid in enc.encode(text)])
    assert reconstructed == expected

def test_tokenizer_empty_string():
    tokenizer = Tokenizer()
    assert tokenizer.get_string_tokens("") == []
