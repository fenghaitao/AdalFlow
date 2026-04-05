## 2025-05-15 - [Regex pre-compilation and Set lookups in functional.py]
**Learning:** Compiling regex inside frequently called functions (like JSON/YAML extractors) and O(N) list lookups in recursive functions (like `custom_asdict`) are significant but easily fixed bottlenecks in utility-heavy libraries.
**Action:** Always pre-compile regex at the module level and prioritize sets over lists for membership checks in performance-sensitive recursive functions.
