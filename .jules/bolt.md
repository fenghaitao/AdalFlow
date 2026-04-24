## 2025-05-15 - [O(N^2) Bottleneck in Prompt rendering]
**Learning:** In `Prompt._deep_render`, creating a filtered copy of `kwargs` on every call leads to $O(N^2)$ complexity relative to the number of keyword arguments. This is particularly noticeable when using `Generator` or `Prompt` with many variables (e.g., in complex RAG or agentic workflows).
**Action:** Pre-filter context once before recursive rendering passes and pass the pre-filtered dictionary down. Always consider if a dictionary operation inside a loop over the same dictionary's keys is creating an $O(N^2)$ situation.
