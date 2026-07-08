## 2025-05-15 - [Tiktoken Batch Decoding Optimization]
**Learning:** In `tiktoken`, calling `decode([token_id])` in a loop for each token is significantly slower than using `decode_tokens_bytes(token_ids)` in batch. The latter reduces function call overhead and is optimized for bulk operations. Benchmarking showed a ~33% speedup for large texts (1000x repeat of a sentence).
**Action:** Always prefer `decode_tokens_bytes` followed by a list comprehension for string decoding when processing multiple token IDs at once.
