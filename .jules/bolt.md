## 2025-05-15 - Optimized Prompt rendering complexity
**Learning:** `Prompt._convert_prompt_kwargs_to_str` had an O(N^2) bottleneck because it was pre-filtering the context dictionary inside `_deep_render`, which was called for every item in the dictionary. For large prompt contexts (e.g., 2000 items), this resulted in significant latency (~1.1s).
**Action:** Pre-filter the context dictionary once before the loop and pass the filtered result to `_deep_render`. This reduces complexity to O(N) and yielded a ~500x speedup (~1.1s to ~0.002s) for 2000 keyword arguments.
