## 2025-05-15 - [O(N) Prompt Keyword Rendering]
**Learning:** Identifying O(N^2) bottlenecks in core rendering loops is critical for performance in LLM frameworks. In AdalFlow, `Prompt._convert_prompt_kwargs_to_str` was filtering the entire context dictionary for every keyword argument during deep rendering, leading to quadratic time complexity. Pre-filtering the context once and passing it down to the rendering function achieved a ~500x speedup for 2000 keyword arguments (from 1.14s to 0.002s).

**Action:** Always check if filtering or searching through large dictionaries/lists happens inside a loop. If the filter criteria don't change per iteration, move the filtering outside the loop and pass the result.
