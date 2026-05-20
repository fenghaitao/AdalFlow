## 2025-05-15 - Robust and fast JSON extraction with JSONDecoder
**Learning:** Manual character-by-character brace counting in Python is slow (O(N) in Python) and fails when braces/brackets are present inside string literals (correctness bug). Using `json.JSONDecoder().raw_decode()` provides a ~5.6x speedup by leveraging the C-optimized decoder and robustly handles complex JSON syntax including escaping and nested structures.
**Action:** Always prefer `json.JSONDecoder().raw_decode()` over manual counting for extracting JSON or lists from larger text blobs.
