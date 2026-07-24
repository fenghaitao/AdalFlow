# Bolt Performance Journal

## 2025-02-15 - Initial setup
**Learning:** Foundational setup of Bolt performance journal.
**Action:** Always read this file before identifying optimizations.

## 2026-01-20 - Direct recursive conversion vs JSON round-trip
**Learning:** Doing an object serialization/deserialization round-trip (e.g., json.loads(json.dumps(...))) with standard JSON libraries inside python functions is surprisingly slow despite C-level optimization. The roundtrip involves string allocation, formatting (especially with indent options), and regex parsing. Directly traversing the nested python structures recursively is much faster (~2.37x speedup) while maintaining full compatibility.
**Action:** For similar deep-copying or schema conversion patterns, design direct recursive python traversals rather than falling back to serialization format round-trips.
