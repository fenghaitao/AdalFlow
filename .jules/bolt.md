# Bolt's Performance Journal

## 2025-02-17 - [Optimizing serialization round-trip in to_dict]
**Learning:** In AdalFlow, `to_dict` was previously implemented as a round-trip: `json.loads(serialize(obj))`. This created significant overhead, especially on dataclasses and components, since standard JSON serialization has to format fields recursively to JSON strings, execute the python fallback `default(obj)` hooks for custom types, and then parse the entire formatted string back to a Python dict.

Replacing this with a direct recursive walker achieves a 1.6x - 2.0x speedup while preserving full exact compatibility with the JSON structure (e.g. converting dictionary keys to strings, converting sets and specialized types recursively through `default` back into their standardized forms).
**Action:** Always prefer direct recursive conversion walkers over serializing-then-parsing strings when converting complex objects to plain nested structures, while ensuring the custom fallback `default` logic output is also recursively walked to guarantee type consistency.
