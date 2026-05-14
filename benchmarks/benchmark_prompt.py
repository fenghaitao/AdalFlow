import time
from adalflow.core.prompt_builder import Prompt
import logging

# Disable logging for cleaner output
logging.getLogger("adalflow").setLevel(logging.ERROR)

def benchmark_prompt_rendering():
    n_kwargs = 100
    iterations = 1000

    prompt_kwargs = {f"key_{i}": f"value_{i}" for i in range(n_kwargs)}
    prompt = Prompt(template="Template", prompt_kwargs=prompt_kwargs)

    start = time.time()
    for _ in range(iterations):
        prompt._convert_prompt_kwargs_to_str(prompt_kwargs)
    end = time.time()

    print(f"Rendering with {n_kwargs} kwargs took: {end - start:.4f}s for {iterations} iterations")

    n_kwargs_large = 1000
    prompt_kwargs_large = {f"key_{i}": f"value_{i}" for i in range(n_kwargs_large)}
    iterations_large = 100

    start = time.time()
    for _ in range(iterations_large):
        prompt._convert_prompt_kwargs_to_str(prompt_kwargs_large)
    end = time.time()

    print(f"Rendering with {n_kwargs_large} kwargs took: {end - start:.4f}s for {iterations_large} iterations")

if __name__ == "__main__":
    benchmark_prompt_rendering()
