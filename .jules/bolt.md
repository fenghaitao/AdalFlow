## 2025-05-22 - Optimized Dataclass Functional Utilities
**Learning:** Redundant type metadata extraction and field lookups in recursive serialization/deserialization functions like `custom_asdict` and `dataclass_obj_from_dict` create significant overhead for large datasets. Caching static metadata with `lru_cache` and hoisting type checks out of collection loops provide high-leverage performance gains.
**Action:** Always check for redundant computations inside loops or recursions in core utility functions; use `lru_cache` for static type/class metadata.
