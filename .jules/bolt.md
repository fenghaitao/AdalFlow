# Bolt's Performance Journal

## 2026-08-09 - PyYAML CDumper and CSafeLoader C-Extensions
**Learning:** PyYAML's pure-Python implementation is slow for frequent serialization and deserialization. Utilizing `CSafeLoader` and `CDumper` directly yields an approximate 4.4x speedup. However, when custom representers (like for `OrderedDict`) are used, they must be registered specifically on `CDumper` if it is present; otherwise, PyYAML's serializer outputs raw `!!python/object/apply` annotations.
**Action:** Always verify custom representers are registered on BOTH standard and C-extensions, and dynamically resolve `SafeLoader`/`Dumper` with a pure-Python fallback.

## 2026-08-09 - Built-in Random vs NumPy Choice for Small Datasets
**Learning:** For small-to-medium datasets (such as prompt examples, few-shot selectors, or list sampling), `np.random.choice` has massive array-initialization overhead. Using Python's built-in `random.sample` and `random.choices` for standard unweighted and weighted-with-replacement sampling yields a 5.7x speedup.
**Action:** Implement fast-paths using python's built-in `random` module for standard list sampling and only fallback to `numpy` for weighted sampling without replacement.
