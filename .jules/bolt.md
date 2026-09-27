## 2025-05-18 - Pre-compiled Module-Level Regex Patterns in Core Functional Parsers
**Learning:** Functions like `extract_json_str`, `extract_yaml_str`, and primitive string parsers in `adalflow.core.functional` are invoked frequently during LLM output parsing. Re-compiling regexes or calling `re.search`/`re.sub` with raw string patterns inside function calls introduces compilation and cache-lookup overhead on hot paths.
**Action:** Always pre-compile regex patterns as module-level constants (e.g. `_INT_PATTERN`, `_JSON_MARKDOWN_PATTERN`) for frequently executed text parsing utilities.
