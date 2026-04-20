## 2025-05-15 - [Generator] Lazy Prompt Caching and Rendering Optimization

**Learning:** In the AdalFlow `Generator` class, the `Prompt` object was being instantiated repeatedly for every call to `get_prompt`, `print_prompt`, or `_extra_repr`. Since `Prompt` instantiation involves Jinja2 template parsing, this introduced significant overhead (up to ~3.5ms for large templates). Furthermore, the prompt was being rendered twice in the `call` pipeline: once in `call` itself and again in `_pre_call`.

**Action:**
1. Implement a lazy-cached `_prompt_builder` property using `object.__setattr__` to avoid registering the internal builder as a public sub-component.
2. Override `__setattr__` to invalidate the cache when `template` or `prompt_kwargs` are updated.
3. Optimize the `call` and `acall` pipeline to render the prompt exactly once and pass it downstream to `_pre_call`.
4. Benchmarking with a mock client is essential to isolate these local processing overheads from network latency.
