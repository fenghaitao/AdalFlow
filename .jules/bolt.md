# Bolt's Performance Journal
## 2026-04-03 - Optimize Prompt Rendering and Caching
**Learning:** Re-instantiating Jinja2-based Prompt objects and redundant rendering of large templates are significant overheads (O(N^2) filtering and redundant parsing). Caching the builder and passing pre-rendered strings can provide ~100x speedup in hot paths.
**Action:** Always cache reusable components like Prompts and avoid rendering the same template multiple times in a single logical operation.
