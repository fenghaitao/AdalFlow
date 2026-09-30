## 2025-05-20 - ConversationMemory Prompt Instantiation Bottleneck
**Learning:** Instantiating `Prompt(template=...)` inside a component's hot path (like `ConversationMemory.call()`) forces Jinja2 to re-parse template AST and undeclared variables on every single call. Pre-instantiating `Prompt` in `__init__` preserves state management via `Component._components` while cutting call latency by ~300x (~13.4ms/call down to 0.045ms/call).
**Action:** Always pre-instantiate `Prompt` templates as sub-components during `__init__` when writing or refactoring AdalFlow components.
