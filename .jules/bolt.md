## 2025-05-22 - [Optimized O(N^2) to O(N) in Prompt Rendering]
**Learning:** Redundant dictionary filtering inside recursive or repeated calls (like `_deep_render`) can lead to quadratic performance bottlenecks ((N^2)$) as the number of elements increases.
**Action:** Pre-filter the context once at the entry point of the loop or recursion to provide an already cleaned dataset to sub-functions.

## 2025-05-22 - [Improved Prompt Rendering Speed]
**Learning:** Implementing an early exit for common, non-renderable types in deep rendering logic avoids unnecessary `isinstance` checks and recursion overhead.
**Action:** Always check if a value is of a type that actually needs processing (e.g., `Prompt` or `Template`) before entering complex logic.
