## 2026-03-31 - Pre-allocating `estimated_num_tokens` in `TextSplitter`

**Learning:** `Document.__post_init__` automatically counts tokens using `self.tokenizer.count_tokens(self.text)` whenever `estimated_num_tokens` is `None`. When splitting documents with `split_by="token"`, `TextSplitter` has already tokenized the input into token arrays of known lengths (`len(tok_chunk)`). Re-encoding each string chunk inside `Document.__post_init__` doubles the total tiktoken work.
**Action:** When constructing `Document` objects from pre-tokenized chunks, pass `estimated_num_tokens=len(tok_chunk)` directly to bypass redundant token counting in `Document.__post_init__`. Always access `self.tokenizer` rather than `TextSplitter.tokenizer` to preserve instance-level encapsulation.
