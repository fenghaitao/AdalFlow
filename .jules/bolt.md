## 2025-05-15 - Caching Prompt builder in Generator

**Learning:** Re-instantiating the `Prompt` class on every `Generator.call` (or `get_prompt`) is expensive due to Jinja2 template parsing. For large templates, this can add significant overhead (ms range). Additionally, calling `get_prompt` followed by `_pre_call` resulted in double-rendering of the prompt.

**Action:** Cache the `Prompt` instance in `Generator` lazily. Use `object.__setattr__` for internal cache variables to avoid them being registered as sub-components in AdalFlow's recursive state management. Override `__setattr__` to invalidate the cache when `template` or `prompt_kwargs` are modified. Pass the rendered `prompt_str` to `_pre_call` to eliminate redundant rendering.
