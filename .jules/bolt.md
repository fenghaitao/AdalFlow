## 2025-05-22 - [Optimizing Generator prompt rendering]
**Learning:** Redundant prompt rendering in `Generator.call` and `Generator._pre_call` was causing measurable overhead. Additionally, re-instantiating `Prompt` on every `get_prompt` call was extremely expensive (~28x slower than reusing a cached `Prompt` instance).
**Action:** Implement `Prompt` builder caching in `Generator` and pass pre-rendered strings to avoid redundant work.
