# Bolt Performance Journal

## 2025-05-23 - [Prompt Keyword Rendering Complexity]
**Learning:** `Prompt._convert_prompt_kwargs_to_str` had O(N²) complexity due to redundant context filtering in `_deep_render`. Filtering the context once before iterating over keyword arguments yields a ~135x speedup for 800 keys.
**Action:** Always check for redundant dictionary comprehensions or filtering logic inside loops that operate on the same collection. Hoist these operations out of the loop to achieve linear complexity.
