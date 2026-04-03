import time
from adalflow.core.generator import Generator
from adalflow.core.prompt_builder import Prompt
from adalflow.components.model_client.openai_client import OpenAIClient
from unittest.mock import MagicMock

def benchmark_prompt_instantiation():
    template = "Hello {{ name }}! " * 100
    prompt_kwargs = {"name": "World"}

    start_time = time.time()
    for _ in range(1000):
        p = Prompt(template=template, prompt_kwargs=prompt_kwargs)
    end_time = time.time()
    print(f"Prompt instantiation (1000 times): {end_time - start_time:.4f}s")

def benchmark_generator_get_prompt():
    client = MagicMock(spec=OpenAIClient)
    gen = Generator(model_client=client, template="Hello {{ name }}! " * 100)
    prompt_kwargs = {"name": "World"}

    start_time = time.time()
    for _ in range(1000):
        gen.get_prompt(**prompt_kwargs)
    end_time = time.time()
    print(f"Generator.get_prompt (1000 times): {end_time - start_time:.4f}s")

if __name__ == "__main__":
    benchmark_prompt_instantiation()
    benchmark_generator_get_prompt()
