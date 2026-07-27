# Bolt Performance Journal

## 2025-02-15 - Initial Setup
**Learning:** Foundational setup of the performance journal.
**Action:** Keep track of codebase performance characteristics, bottlenecks, and optimizations here.

## 2025-02-15 - [to_dict Optimization]
**Learning:** Performing a serialization round-trip via `json.loads(serialize(obj))` to obtain a dictionary representation of an object introduces significant O(N) string processing and AST generation overhead. A direct recursive python-to-python dictionary/list mapping reduces execution time dramatically (~1.86x faster) while maintaining perfect type compatibility.
**Action:** Use direct recursive type mapping for in-memory object conversions (like `to_dict`) instead of serializing to strings and deserializing back, and recursively invoke the `default` hooks to maintain parity for specialized custom types.
