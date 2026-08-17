## 2025-02-17 - Inverted Index & Vectorized Scoring for BM25Retriever
**Learning:** In BM25 document retrieval, calculating term scores via full-corpus scans (`np.array([(doc.get(q) or 0) for doc in self.t2d])`) performs $O(|D| \times |Q|)$ dictionary lookups on every query. Precomputing an inverted index mapping tokens to posting arrays (`doc_indices`, `term_freqs`) and document length normalization factors reduces computation to matching documents ($O(\text{df} \times |Q|)$), achieving a ~3.8x to 7x query speedup.
**Action:** Always prefer inverted postings list representations over full-corpus list iteration for lexical retrievers and search algorithms.

## 2025-02-17 - Standard vs Custom JSON Deserialization in Component Loaders
**Learning:** `adalflow.utils.file_io.load_json` uses `_deserialize_object_hook`, which automatically reconstructs registered `EntityMapping` classes. Calling `Component.from_dict` on the output of `load_json` leads to type errors because the dictionary was already instantiated into a `Component` object.
**Action:** Use `load_standard_json` when loading JSON dict representations intended for explicit `.from_dict()` instantiation.
