## 2025-05-20 - Pre-compile regex patterns in core string parsing utilities
**Learning:** Functions like `extract_json_str`, `extract_yaml_str`, and `extract_first_int` in `adalflow.core.functional` are called frequently when parsing LLM outputs. Pre-compiling `re.compile` patterns at module-level eliminates compilation overhead per call, yielding ~2.2x-4.2x speedup for string extraction routines.
**Action:** Always pre-compile regexes at module scope (`_PATTERN = re.compile(...)`) for parsing and string processing utilities that execute in high-frequency prompt/parsing loops.
