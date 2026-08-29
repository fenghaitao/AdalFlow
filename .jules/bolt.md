
## 2026-03-30 - Caching Sub-components in Generator

**Learning:** Assigning sub-components like `Prompt` as attributes on `Component` subclasses automatically registers them in `self._components`. When caching `Prompt` in `Generator`, setting `self.prompt.prompt_kwargs = self._prompt_kwargs` guarantees that in-place dictionary mutations on `generator.prompt_kwargs` and dynamic `Parameter` data updates during training loops reflect instantly without re-instantiating `Prompt` or recompiling Jinja2 templates on every call.
**Action:** Always link mutable reference dictionaries on cached sub-components and provide property setters that update the cache when sub-component attributes or templates change.
