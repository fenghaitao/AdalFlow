## 2025-05-22 - [Optimized BM25Retriever Scoring]
**Learning:** Implementing an inverted index (`token -> (np.array(indices), np.array(freqs))`) and precomputing formula constants significantly reduces BM25 scoring complexity from O(Q*N) to O(Q*avg_df). In this codebase, `Component.from_dict` (via `__new__`) bypasses `__init__`, so default internal states (like `_components`, `training`, etc.) MUST be manually initialized during deserialization if not present in the saved state to avoid `AttributeError`.

**Action:** Always use inverted indices for term-based retrieval. Ensure any custom deserialization logic handles the `Component` base class's state initialization correctly when using `__new__`.
