# Bolt's Performance Journal ⚡

## 2025-05-22 - [Correctness vs. Speed in JSON Parsing]
**Learning:** Manual character-by-character loops in Python for brace counting in JSON strings are not only slow (O(N) with high constant factor) but often incorrect when braces appear inside string literals. Using the standard library's `json.JSONDecoder().raw_decode` leverages C-optimized parsing, which is significantly faster and handles string literals correctly. However, `raw_decode` does not support incomplete JSON, so a fallback is necessary for features like `add_missing_right_brace`.
**Action:** Always prefer standard library C-optimized parsers (`json`, `yaml`) over manual string manipulation for structured data, but maintain robust fallbacks for "lenient" parsing requirements.
