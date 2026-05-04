## 2025-05-22 - [O(N²) bottleneck in Prompt keyword processing]
**Learning:** `Prompt._convert_prompt_kwargs_to_str` exhibited O(N²) complexity because it iterated over all keyword arguments and performed an O(N) context filtering operation inside the loop. This resulted in significant latency (~2.8s for 1000 kwargs).
**Action:** Implement an O(N) fast-path check to skip recursive rendering for simple keyword arguments and move context filtering outside the loop for complex ones. This yielded a ~225x speedup.
