# Bolt Performance Journal

## 2026-07-26 - Pre-compiling Regex Patterns in Hot LLM Response Parsing Paths
**Learning:** Dynamic inline regex compiling (via `re.compile` or passing string regex patterns repeatedly to `re.search`) inside core parsing utility functions is a significant anti-pattern in LLM frameworks. Because model clients and generators repeatedly invoke string parsing utilities (such as `extract_json_str` and `extract_first_int`) to process LLM outputs, inline regex compilation repeatedly incurs pattern parsing and caching lookup overhead. Moving these patterns to module-level constants yields a ~54% to ~71% reduction in string parsing execution overhead.
**Action:** Always pre-compile regex patterns as module-level constants in files containing hot path string parsing, token extraction, or text validation utility functions.
