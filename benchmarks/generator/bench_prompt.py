import time
from adalflow.core.prompt_builder import Prompt

template = "Hello {{name}}, welcome to {{place}}!"
kwargs = {"name": "Bolt", "place": "the fast lane"}

start = time.perf_counter()
for _ in range(1000):
    p = Prompt(template=template)
    _ = p.call(**kwargs)
end = time.perf_counter()
print(f"Time for 1000 instantiations + calls: {end - start:.4f}s")

p = Prompt(template=template)
start = time.perf_counter()
for _ in range(1000):
    _ = p.call(**kwargs)
end = time.perf_counter()
print(f"Time for 1000 calls (cached prompt): {end - start:.4f}s")
