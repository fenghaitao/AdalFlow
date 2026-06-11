## 2025-05-22 - [JSON Extraction Optimization]
**Learning:** Manual character-by-character brace counting for JSON extraction is not only O(N) in Python (slow for large payloads) but also prone to bugs when braces appear inside JSON string literals. `json.JSONDecoder().raw_decode` is a much faster (C-implemented) and correct alternative.
**Action:** Use `json.JSONDecoder().raw_decode` for extracting JSON objects/arrays from larger text blocks to ensure correctness and performance.
