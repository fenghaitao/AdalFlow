
import time
import logging
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient
from adalflow.core.types import GeneratorOutput

# Mock ModelClient
class MockClient(ModelClient):
    def call(self, api_kwargs, model_type):
        return "mocked response"
    def parse_chat_completion(self, completion):
        return GeneratorOutput(raw_response=completion, data=completion)
    def convert_inputs_to_api_kwargs(self, input, model_kwargs, model_type):
        return {"model": model_kwargs.get("model"), "prompt": input}

def benchmark_generator():
    template = "Template with some variables: {{var1}}, {{var2}}, {{var3}}"
    prompt_kwargs = {"var1": "value1", "var2": "value2", "var3": "value3"}
    generator = Generator(
        model_client=MockClient(),
        model_kwargs={"model": "test-model"},
        template=template,
        prompt_kwargs=prompt_kwargs
    )

    # Benchmark get_prompt
    start_time = time.time()
    for _ in range(1000):
        generator.get_prompt()
    end_time = time.time()
    print(f"Time for 1000 get_prompt calls: {end_time - start_time:.4f}s")

    # Benchmark call (mocked)
    generator.mock_output = True
    start_time = time.time()
    for _ in range(1000):
        generator.call(prompt_kwargs={"var1": "new_value"})
    end_time = time.time()
    print(f"Time for 1000 generator calls: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    benchmark_generator()
