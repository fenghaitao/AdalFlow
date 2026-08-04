# Bolt's Performance Journal

This journal tracks critical performance learnings, bottlenecks, and optimizations within AdalFlow.

## 2026-01-20 - PyYAML C-extensions and OrderedDict Representers
**Learning:** PyYAML's C-extension Loader (`CSafeLoader`) is ~5.5x faster, and Dumper (`CDumper`) is ~3.3x faster than their pure-Python counterparts. However, custom class representers (like `collections.OrderedDict`) must be explicitly registered on the `CDumper` class itself, or the dumper will serialize them as raw `!!python/object/apply` python annotations.
**Action:** Always register custom representers on `yaml` AND the dynamically-selected `CDumper` (or fallbacks) in serialization files (e.g., `base_data_class.py`).

## 2026-01-20 - Tiktoken get_string_tokens Fast-path
**Learning:** For `tiktoken`, looping over token IDs and calling `.decode([token_id])` incurs noticeable loop overhead. Using `decode_single_token_bytes` combined with a string decode (.decode('utf-8', errors='replace')) provides a 2x-3x speedup.
**Action:** Use `getattr(self.tokenizer, 'decode_single_token_bytes', None)` as a fast path with safe loop-fallback for generic backends.
