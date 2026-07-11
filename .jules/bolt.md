## 2025-05-22 - [Optimize Regex Parsing]
**Learning:** Pre-compiling regex patterns as module-level constants significantly improves performance for frequent LLM output parsing tasks (JSON, YAML, numbers). Benchmarking showed a ~33-38% improvement compared to inline `re.search` or `re.compile` calls within functions.
**Action:** Always pre-compile frequently used regex patterns in core utility modules.

## 2025-05-22 - [Tokenizer String Tokens Overhead]
**Learning:** For `tiktoken`, using `decode_bytes([token_id]).decode("utf-8")` is ~30% faster than `decode([token_id])` for individual token IDs due to less internal overhead in the `tiktoken` library. However, this is specific to `tiktoken` and might break other tokenizer implementations.
**Action:** Be cautious with library-specific optimizations in generic wrapper classes to maintain compatibility.
