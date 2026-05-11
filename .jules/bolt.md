## 2025-05-22 - [Dataclass field lookup caching]
**Learning:** Calling `dataclasses.fields()` repeatedly, especially in recursive serialization paths like `custom_asdict`, introduces measurable overhead because it introspects the class and creates a new tuple every time.
**Action:** Use a module-level `weakref.WeakKeyDictionary` to cache the result of `fields(cls)`. Using `weakref` prevents memory leaks when classes are dynamically created.
