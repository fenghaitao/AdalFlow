
import time
import unittest.mock as mock
from adalflow.core.generator import Generator
# from adalflow.components.model_client.openai_client import OpenAIClient
from adalflow.core.model_client import ModelClient

class MockClient(ModelClient):
    def init_sync_client(self): return None
    def init_async_client(self): return None
    def call(self, **kwargs): return None
    async def acall(self, **kwargs): return None
    def parse_chat_completion(self, completion): return None
    def convert_inputs_to_api_kwargs(self, **kwargs): return {}

def benchmark_prompt_creation():
    template = "Hello {{ name }}! Today is {{ day }}."
    prompt_kwargs = {"name": "Bolt", "day": "Monday"}

    start_time = time.perf_counter()
    for _ in range(10000):
        from adalflow.core.prompt_builder import Prompt
        prompt = Prompt(template=template, prompt_kwargs=prompt_kwargs)
        _ = prompt.call()
    end_time = time.perf_counter()
    print(f"Time for 10000 Prompt creations and calls: {end_time - start_time:.4f}s")

def benchmark_generator_get_prompt():
    client = MockClient()
    generator = Generator(
        model_client=client,
        model_kwargs={"model": "gpt-3.5-turbo"},
        template="Hello {{ name }}! Today is {{ day }}.",
        prompt_kwargs={"name": "Bolt", "day": "Monday"}
    )

    start_time = time.perf_counter()
    for _ in range(10000):
        _ = generator.get_prompt()
    end_time = time.perf_counter()
    print(f"Time for 10000 generator.get_prompt() calls: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    benchmark_prompt_creation()
    benchmark_generator_get_prompt()
