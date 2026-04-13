## 2025-05-15 - [Prompt builder caching in Generator]
**Learning:** Instantiating a `Prompt` object in AdalFlow is relatively expensive (~4.6ms for large templates) because it triggers Jinja2 template parsing. The `Generator` class was instantiating `Prompt` multiple times per call, leading to significant overhead.
**Action:** Cache the `Prompt` instance within the `Generator` class and reuse it across `get_prompt`, `print_prompt`, and `_extra_repr` calls. Ensure cache invalidation by checking the identity of `template` and `prompt_kwargs`.
