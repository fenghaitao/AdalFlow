## 2026-03-31 - Lazy Singleton Tokenizer for Hot Document / Tokenization Paths
**Learning:** Instantiating `Tokenizer()` on every `Document` creation (`__post_init__`, `from_dict`) or during helper tokenization functions in `BM25Retriever` causes thousands of redundant `Tokenizer` object allocations and `tiktoken.get_encoding` wrapper calls during batch data processing.
**Action:** Use `get_default_tokenizer()` (a lazy module-level singleton) for default token counting and string tokenization across data models and retrieval helper functions.
