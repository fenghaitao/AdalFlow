## 2025-05-14 - [Regex Optimization in hot utility functions]
**Learning:** Pre-compiling regex patterns as module-level constants in `functional.py` provides significant performance gains (e.g., ~4x speedup for `extract_yaml_str` and ~37% for `extract_json_str`) by avoiding redundant re-compilation during frequent LLM output parsing calls.
**Action:** Always pre-compile regex patterns as module-level constants when they are used in high-frequency utility functions or components involved in data parsing.
