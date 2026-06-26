## 2025-05-15 - [O(N^2) complexity in Prompt rendering context]
**Learning:** The prompt rendering logic was performing an O(N) filter of the context dictionary inside an O(N) loop over all prompt keyword arguments. This led to O(N^2) complexity for context preparation, causing significant lag (~1s) when prompts had many variables (e.g., 2000).
**Action:** Always pre-calculate filtered contexts or metadata once before entering a processing loop over the same data.

## 2025-05-15 - [Redundant Regex Compilation]
**Learning:** Frequently used utility functions like `extract_json_str` and `extract_first_int` were compiling regex patterns on every call. While Python's `re` module has an internal cache, explicit module-level compilation is faster (~3x) and more predictable.
**Action:** Pre-compile all regex patterns at the module level for performance-critical utility functions.
