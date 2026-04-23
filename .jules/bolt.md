## 2025-05-14 - [Generator Prompt Caching]
**Learning:** Instantiating `Prompt` objects and parsing Jinja2 templates is expensive (~0.6-1.0ms per instantiation). `Generator` was doing this multiple times per call, significantly increasing overhead.
**Action:** Use a lazy-loaded property to cache the `Prompt` builder in the parent component and use `__setattr__` for cache invalidation. Pass the rendered prompt string downstream to avoid redundant rendering.
