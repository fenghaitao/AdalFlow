## 2025-05-15 - [Optimization of to_dict via direct recursion]
**Learning:** The `to_dict` utility was previously using a `json.loads(serialize(obj))` round-trip, which was extremely inefficient as it involved stringifying the entire object tree and then parsing it back. Replacing this with a direct recursive conversion provided a ~5x-20x speedup depending on the object complexity.
**Action:** Always look for JSON round-trips used for deep cloning or dictionary conversion, as they are a common performance bottleneck in Python.
