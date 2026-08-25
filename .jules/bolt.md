## 2026-03-08 - Document token estimation bypass in TextSplitter
**Learning:** `Document.__post_init__` calls `Tokenizer().count_tokens(self.text)` whenever `estimated_num_tokens` is None. For `split_by="token"` in `TextSplitter`, chunk token counts are already known during splitting.
**Action:** When producing `Document` chunks from token-based splitters, pass `estimated_num_tokens` directly to bypass redundant tiktoken encoding calls (~2.4x speedup for document chunking).
