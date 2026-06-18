## 2025-05-15 - [Robust and Fast JSON/List Extraction]
**Learning:** Manual character-by-character scanning for JSON/List boundaries in Python is significantly slower than C-based decoders for large payloads and frequently fails when delimiters (braces/brackets) appear within string literals.
**Action:** Utilize `json.JSONDecoder().raw_decode(text, start_index)` to accurately and efficiently find the end of a JSON block. Implement a manual counting fallback only to support partial/incomplete strings (e.g., from streaming LLM responses) when the `add_missing_delimiter` flag is enabled.
