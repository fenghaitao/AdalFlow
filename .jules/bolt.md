# Bolt's Journal - Critical Learnings

## 2025-05-15 - Token Count Caching in TextSplitter Document Instantiation
**Learning:** `Document.__post_init__` automatically recalculates token counts using `Tokenizer().count_tokens(text)` if `estimated_num_tokens` is not explicitly provided. When `TextSplitter` chunks documents by token (`split_by="token"`), the chunks are already token lists before being decoded to strings. Passing `estimated_num_tokens=len(chunk)` directly to `Document(...)` prevents redundant tiktoken re-tokenization.
**Action:** When creating `Document` instances from pre-tokenized content, explicitly supply `estimated_num_tokens` to bypass redundant token counting overhead.
