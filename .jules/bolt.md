## 2025-05-15 - Caching internal Prompt builder in Generator

**Learning:** Re-instantiating `Prompt` objects (which involves Jinja2 environment setup and template parsing) on every `get_prompt` or `call` is a significant bottleneck, especially for large templates (~2.3ms overhead per call). Additionally, rendering the prompt twice in `call`/`acall` (once for logging/tracing and once in `_pre_call`) adds another ~2.3ms for large templates.

**Action:** Cache the `Prompt` instance in `Generator` and ensure safe cache invalidation by overriding `__setattr__`. Use `object.__delattr__` and `super().__setattr__` to manage internal state without triggering `Component`'s automatic child registration. Pass the rendered prompt string to `_pre_call` to avoid redundant rendering.
