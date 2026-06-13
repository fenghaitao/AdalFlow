## 2025-05-15 - [Optimized JSON and List Extraction]
**Learning:** Manual character-by-character brace/bracket counting for JSON extraction is not only slow (O(N) in Python) but also incorrect when those delimiters appear inside string literals. Using `json.JSONDecoder().raw_decode()` provides a significant speedup (up to ~17x) by leveraging C-implemented parsing and correctly handles JSON syntax.

**Action:** Prefer `json.JSONDecoder().raw_decode()` for finding the boundaries of JSON-like structures in text. Always provide a manual fallback for cases where the JSON is incomplete but can be salvaged by adding missing delimiters.
