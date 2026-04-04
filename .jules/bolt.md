## 2025-05-15 - [Optimization of functional utilities]
**Learning:** Compiling regex patterns inside frequently called functions (like JSON/YAML extraction) adds redundant overhead. Converting exclusion lists to sets for lookups significantly improves performance in recursive data structures.
**Action:** Always pre-compile regex patterns at the module level. Use sets for O(1) lookups when checking for membership in exclusion or inclusion lists, especially in recursive operations.
