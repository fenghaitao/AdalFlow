## 2025-02-16 - Pre-compiling Regex Patterns in Functional String Parsing Functions

**Learning:** Dynamic calls to `re.compile()` within hot string-parsing paths (such as `extract_json_str`, `extract_yaml_str`, `extract_first_int`, `extract_first_boolean`, `extract_first_float`, and `fix_json_missing_commas`) cause redundant regex compilation and internal cache lookup overhead during repetitive LLM output processing.
**Action:** Always pre-compile static regular expressions as module-level private constants (e.g. `_INT_PATTERN = re.compile(...)`) when functions are expected to be invoked frequently in data processing or LLM response parsing pipelines.
