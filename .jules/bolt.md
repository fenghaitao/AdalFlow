## 2025-05-18 - Pre-filtering Prompt Rendering Context Dict

**Learning:** In `Prompt._convert_prompt_kwargs_to_str`, `_deep_render` was constructing `filtered_kwargs` on every single iteration across kwargs, turning prompt context preparation into an $O(N^2)$ operation. Pre-filtering the `context_for_render` dictionary once outside the loop and passing it into `_deep_render` reduces complexity to $O(N)$ and returns early for non-Prompt/Template values, yielding a ~500x speedup for large context dictionaries.

**Action:** When rendering or processing dictionary elements recursively or in a loop, always pre-filter or pre-compute invariant context structures outside the iteration loop.
