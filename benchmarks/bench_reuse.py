
import time
from adalflow.core.prompt_builder import Prompt
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient

class MockClient(ModelClient):
    def init_sync_client(self): return None
    def init_async_client(self): return None
    def call(self, **kwargs): return None
    async def acall(self, **kwargs): return None
    def parse_chat_completion(self, completion): return None
    def convert_inputs_to_api_kwargs(self, **kwargs): return {}

def benchmark_reused_prompt():
    template = "Hello {{ name }}! Today is {{ day }}."
    prompt_kwargs = {"name": "Bolt", "day": "Monday"}
    prompt = Prompt(template=template, prompt_kwargs=prompt_kwargs)

    start_time = time.perf_counter()
    for _ in range(10000):
        _ = prompt.call()
    end_time = time.perf_counter()
    print(f"Time for 10000 reused Prompt calls: {end_time - start_time:.4f}s")

def benchmark_new_prompt():
    template = "Hello {{ name }}! Today is {{ day }}."
    prompt_kwargs = {"name": "Bolt", "day": "Monday"}

    start_time = time.perf_counter()
    for _ in range(10000):
        prompt = Prompt(template=template, prompt_kwargs=prompt_kwargs)
        _ = prompt.call()
    end_time = time.perf_counter()
    print(f"Time for 10000 new Prompt creations and calls: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    benchmark_reused_prompt()
    benchmark_new_prompt()
