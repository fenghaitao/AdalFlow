## 2025-05-15 - Caching sub-components in Generator
**Learning:** Instantiating sub-components like `Prompt` inside the hot path (e.g., `get_prompt`) introduces significant overhead (~1.4ms vs ~0.05ms). Caching them in `__init__` is a major win. However, in AdalFlow, assigning a `Component` to an attribute automatically registers it as a child. This means it shouldn't be manually added to `_extra_repr` to avoid redundant output in `__repr__`.
**Action:** Always cache frequently used DataComponents in the parent's `__init__` and rely on the framework's recursive `__repr__` for visualization.
