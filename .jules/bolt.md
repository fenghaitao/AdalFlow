## 2025-05-21 - Optimized Prompt Rendering O(N^2) to O(N)
**Learning:** In `Prompt._convert_prompt_kwargs_to_str`, the code was filtering the entire context dictionary for every variable being rendered in `_deep_render`, leading to $O(N^2)$ complexity relative to the number of keyword arguments.
**Action:** Pre-filter the context dictionary once and pass it to `_deep_render` to maintain linear $O(N)$ complexity.
