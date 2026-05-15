## 2025-05-14 - Optimized Prompt rendering complexity
**Learning:** Rendering prompts with many keyword arguments suffered from (N^2)$ complexity due to redundant context filtering in recursive rendering logic.
**Action:** Implement a fast-path for non-recursive cases and pre-filter context once for recursive cases to achieve (N)$ scaling.
