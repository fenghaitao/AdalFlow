import time
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient

class MockModelClient(ModelClient):
    def call(self, api_kwargs, model_type):
        return "mock response"
    def parse_chat_completion(self, completion):
        from adalflow.core.types import GeneratorOutput
        return GeneratorOutput(raw_response=completion)
    def convert_inputs_to_api_kwargs(self, input, model_kwargs, model_type):
        return {"input": input}

model_client = MockModelClient()
template = "Hello {{name}}!"

# Measurement 1: Current Generator (creates Prompt inside get_prompt/print_prompt/etc)
gen = Generator(model_client=model_client, template=template)

start = time.perf_counter()
for _ in range(1000):
    _ = gen.get_prompt(name="Bolt")
end = time.perf_counter()
print(f"Time for 1000 get_prompt calls: {end - start:.4f}s")

start = time.perf_counter()
for _ in range(1000):
    _ = gen.call(prompt_kwargs={"name": "Bolt"})
end = time.perf_counter()
print(f"Time for 1000 generator calls: {end - start:.4f}s")
