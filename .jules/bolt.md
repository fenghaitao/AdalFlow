## 2026-03-25 - Prompt Instantiation and Double-Rendering Optimization
**Learning:** Jinja2 template parsing during Prompt instantiation is a significant bottleneck (~1ms+). In Generator.call/acall, the prompt was being rendered twice: once for the tracing span and once in _pre_call, each time creating a new Prompt instance.
**Action:** Cache the Prompt instance in Generator._prompt_builder and use identity-based invalidation (is) for template and prompt_kwargs. Pass the pre-rendered prompt_str to _pre_call to eliminate redundant rendering and parsing, yielding a ~6x speedup in call overhead.
