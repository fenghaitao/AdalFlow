## 2025-05-22 - [Generator Prompt Caching]
**Learning:** Instantiating `Prompt` objects (which involves Jinja2 environment setup and template parsing) is a major bottleneck in `Generator.call` and `get_prompt`, especially for large templates. Re-rendering the prompt multiple times during a single call further compounds this latency.
**Action:** Always cache the `Prompt` instance within orchestrator components like `Generator` and ensure that pre-rendered prompt strings are passed down the call chain to avoid redundant rendering.
