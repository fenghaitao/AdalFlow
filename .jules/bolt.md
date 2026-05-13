## 2025-05-19 - Optimized JSON and List String Extraction
**Learning:** Manual character counting to find matching braces/brackets in strings is O(N) in Python and fails when those characters appear inside string literals. Using `json.JSONDecoder().raw_decode` handles string literals correctly and is significantly faster (up to 80x for large inputs) as it leverages the underlying C implementation.
**Action:** Prefer `json.JSONDecoder().raw_decode` for extracting structured data from text, using manual counting only as a fallback for incomplete/malformed inputs that need auto-correction.
