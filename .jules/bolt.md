# Bolt's Performance Journal

## 2025-05-15 - Fixing O(N²) complexity in Prompt rendering

**Learning:** Repeatedly filtering a large dictionary of keyword arguments inside a loop leads to O(N²) complexity. In AdalFlow's `Prompt._convert_prompt_kwargs_to_str`, this was causing significant latency (up to 30 seconds for 1000 arguments) because each `_deep_render` call was recreating a filtered copy of all kwargs.

**Action:** Pre-filter the keyword arguments once if any nested `Prompt` or `Template` objects are detected. Implement a fast-path using a length comparison to skip the second pass entirely when no nested templates are present. This reduced latency for 1000 arguments from ~29.4s to ~0.04s (~660x speedup).
