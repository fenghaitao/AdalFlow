## 2026-03-06 - [Eliminated Redundant Prompt Rendering]
**Learning:** In the `Generator` class, the prompt was being rendered twice: once for tracing/caching at the start of `call`/`acall`, and again inside `_pre_call`. For complex Jinja2 templates, this adds unnecessary latency to every LLM request.
**Action:** Pass the already-rendered prompt string to internal helper methods like `_pre_call` to avoid re-computation.
