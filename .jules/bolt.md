# Bolt Performance Journal ⚡

## 2025-05-15 - [Optimize to_dict in serialization.py]
**Learning:** The previous implementation of `to_dict` used a `json.loads(serialize(obj))` round-trip, which is extremely inefficient due to full JSON encoding and decoding. A direct recursive conversion is significantly faster (~3.4x improvement). Additionally, when implementing recursive serialization, the results of the `default(obj)` hook must also be recursively processed to handle nested custom types and ensure all results (like tuples) are converted to JSON-compatible formats (like lists).
**Action:** Always prefer direct recursive traversal over serialization round-trips for converting objects to dictionaries. Ensure that all branches of the recursion produce JSON-serializable types (e.g., converting sets and tuples to lists/dicts). Avoid local imports in recursive hot paths.
