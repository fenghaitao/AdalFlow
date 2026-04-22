## 2026-04-22 - Expensive Jinja2 parsing in Generator
**Learning:** Instantiating a `Prompt` object in AdalFlow is computationally expensive (~3.5ms) because it parses the Jinja2 template every time. The `Generator` class was creating a new `Prompt` instance on every call and rendering it twice (once for the span/logging and once for the model call), leading to ~7ms of avoidable overhead per LLM call.
**Action:** Cache the `Prompt` instance within the `Generator` and reuse the rendered prompt string to eliminate double-rendering.
