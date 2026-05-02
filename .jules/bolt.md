## 2025-05-15 - [Component.__setattr__ optimization]
**Learning:** `Component.__setattr__` is a high-frequency method where even minor overheads like nested function definitions or redundant dictionary lookups accumulate significantly. Using `object.__setattr__` bypasses standard `setattr` logic and is much faster for simple attribute assignments.
**Action:** Always consider `object.__setattr__` for internal state management in base classes where standard attribute registration logic isn't needed.

## 2025-05-15 - [Prompt keyword rendering optimization]
**Learning:** Rendering complex objects within prompt templates can lead to O(N²) complexity if not handled carefully, especially when templates are nested. Pre-filtering and fast-path checks for non-template strings provide massive speedups.
**Action:** Use fast-path checks (e.g. string length comparison or type checking) to skip expensive recursive operations when they aren't strictly necessary.
