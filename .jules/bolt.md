## 2025-05-15 - Optimize Generator Prompt Rendering

**Learning:** Re-instantiating the `Prompt` class in every `Generator.call` or `get_prompt` invocation is a significant bottleneck. Each instantiation triggers Jinja2 template parsing and variable discovery, which is expensive (up to ~22ms for large templates). Furthermore, the original `call` and `acall` methods were rendering the prompt twice: once for the tracing span and again within `_pre_call`.

**Action:** Cache the `Prompt` instance within the `Generator` class and use a lazy getter (`_get_prompt_builder`) that invalidates the cache only when the template or `prompt_kwargs` identity changes. Update `_pre_call` to accept an optional `prompt_str` to eliminate redundant rendering. This combination reduced `get_prompt` latency by ~85x and total `call` latency by ~73x for large templates.
