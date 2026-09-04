## 2025-05-20 - Pre-compiling Regexes in Output Parsing
**Learning:** Compiling regular expressions inside utility functions called thousands of times per LLM generation cycle (e.g., `extract_json_str`, `extract_yaml_str`, `extract_first_int`) creates measurable compilation and lookup overhead.
**Action:** Pre-compile all fixed regex patterns as module-level private constants (e.g., `_INT_PATTERN`, `_YAML_RE_PATTERN`) in core parsing modules.
