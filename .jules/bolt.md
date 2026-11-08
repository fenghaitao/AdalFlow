## 2026-03-06 - [Eliminated Redundant Prompt Rendering in Generator]
**Learning:** In the `Generator` class, the prompt template was being rendered twice: once for tracing/caching at the start of `call`/`acall`, and again inside `_pre_call`. For Jinja2 templates and prompt kwargs, this adds redundant template processing latency to every LLM request.
**Action:** Pass the already-rendered prompt string to internal helper methods like `_pre_call` while providing a default fallback (`prompt_str: Optional[str] = None`) to preserve backward compatibility.
