## 2026-06-20 - [O(N^2) Prompt Context Bottleneck]
**Learning:** In the `Prompt` class, `_deep_render` was performing a dictionary comprehension to filter keyword arguments for *every* keyword argument processed, leading to (N^2)$ complexity.
**Action:** Pre-filter context once before the rendering loop and pass the filtered dictionary to recursive calls to maintain (N)$ linear complexity.
