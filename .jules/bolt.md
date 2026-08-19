# Bolt's Performance Journal

## Critical Learnings

- In `tiktoken`, `decode_tokens_bytes(token_ids)` for batch processing is significantly more efficient than calling `decode([token_id])` in a loop.
- Precomputing document length normalization factors and constructing inverted index in `BM25Retriever` avoids O(|D| * |Q|) full corpus dictionary lookups during queries.
- Pre-compiling regex patterns as module-level constants in functional parsers avoids regex re-compilation overhead during LLM output parsing.
- Using `CSafeLoader` and `CDumper` for PyYAML when available speeds up YAML operations by 3-5x. Custom representers (e.g. for OrderedDict) must be registered on `CDumper` as well.
- In `TextSplitter` with `split_by="token"`, passing `estimated_num_tokens=len(tok_chunk)` directly when instantiating chunk `Document` objects avoids redundant re-encoding with tiktoken in `Document.__post_init__`, resulting in a ~2x speedup during batch document chunking.
