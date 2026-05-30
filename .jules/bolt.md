## 2025-05-22 - [Optimized Prompt Rendering Complexity]
**Learning:** The `Prompt._convert_prompt_kwargs_to_str` method had O(N²) complexity because it was re-filtering the entire context dictionary for every keyword argument during rendering.
**Action:** Pre-filter the context once and pass it as an optional argument to `_deep_render` to achieve O(N) complexity.
