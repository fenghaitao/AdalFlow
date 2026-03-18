
## 2026-03-18 - [Generator] Redundant Prompt Rendering and Object Instantiation
**Learning:** Jinja2 template parsing in `Prompt.__init__` is a significant bottleneck (~7.4ms). `Generator` was instantiating and rendering `Prompt` 2-3 times per call, adding ~15-22ms of pure orchestration overhead. Caching the `Prompt` builder and reusing the pre-rendered string reduced overhead to ~0.24ms.
**Action:** Always cache template builders like `Prompt` and pass pre-rendered strings to downstream methods (`_pre_call`, `BackwardContext`) to avoid redundant rendering.
