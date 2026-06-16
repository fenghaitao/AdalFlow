## 2026-06-16 - [Optimizing JSON Extraction]
**Learning:** Using `json.JSONDecoder().raw_decode` for extracting JSON blocks from text is significantly faster (~3.4x for large payloads) and more robust than manual character counting. Manual counting fails when braces or brackets appear inside string literals, a common occurrence in LLM outputs.
**Action:** Prefer built-in decoders with `raw_decode` for block extraction from strings. Always provide a fallback for incomplete blocks if 'repair' functionality (like adding missing closing braces) is required.
