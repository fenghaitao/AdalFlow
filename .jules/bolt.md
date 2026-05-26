## 2025-05-22 - [Generator Prompt Caching]
**Learning:** Caching internal components like `Prompt` in a class that inherits from `Component` (like `Generator`) requires using `object.__setattr__` to avoid they being added to `self._components` registry, which would affect serialization and `repr`.
**Action:** Always use `object.__setattr__` for internal, non-registrable state in `Component`-based classes.

## 2025-05-22 - [Avoiding Redundant Rendering]
**Learning:** In LLM orchestration, rendering the prompt once for logging/tracing and then again for the actual API call is a common bottleneck. Passing the pre-rendered string to internal preparation methods avoids this O(N) overhead.
**Action:** Ensure internal preparation methods (like `_pre_call`) can accept an already rendered prompt string.
