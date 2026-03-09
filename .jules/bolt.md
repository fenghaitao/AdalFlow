## 2025-05-15 - [Generator] Caching Prompt builder and passing pre-rendered prompt string

**Learning:** Performance bottleneck identified in `Generator` where it was creating a new `Prompt` instance and re-rendering the same prompt string multiple times during a single `call`/`acall`. `Prompt` instantiation is expensive because it involves Jinja2 template parsing and variable discovery.

**Action:**
1. Implement `_get_prompt_builder` in `Generator` to cache the `Prompt` instance, invalidating only when `template` or `prompt_kwargs` (via identity) changes.
2. Update `_pre_call` to accept an optional `prompt_str` and pass it from `call`/`acall` to avoid redundant rendering (as it's already rendered for tracing).
3. Measured ~37x speedup in `get_prompt` micro-benchmark (from ~10s to ~0.26s for 10k calls).
