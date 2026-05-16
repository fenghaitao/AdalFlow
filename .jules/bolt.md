## 2024-05-20 - Optimize Component.__setattr__ performance
**Learning:** Local imports and inner function definitions in high-frequency methods like `__setattr__` introduce significant overhead in Python. Caching the class reference in a module-level variable and inlining the logic provided a ~2x speedup.
**Action:** Always avoid local imports and inner function definitions in methods that are called frequently in a loop or at the core of the framework's state management.
