## 2026-06-15 - [Optimize Dataclass Serialization/Deserialization]
**Learning:** Hoisting type checks and using comprehensions for collection restoration significantly reduces overhead in recursive dataclass processing. Pre-processing exclude lists into sets transforms O(N) field lookups into O(1), which is critical for large, nested objects.
**Action:** Always check for repeated type inspection or conditional logic inside loops when processing collections in recursive functions. Use lru_cache for static type analysis functions.
