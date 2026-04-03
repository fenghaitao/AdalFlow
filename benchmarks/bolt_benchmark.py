import time
import jinja2
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient
from adalflow.core.prompt_builder import Prompt

class MockModelClient(ModelClient):
    def call(self, api_kwargs, model_type):
        return "mock response"
    def parse_chat_completion(self, completion):
        from adalflow.core.types import GeneratorOutput
        return GeneratorOutput(raw_response=completion)
    def convert_inputs_to_api_kwargs(self, input, model_kwargs, model_type):
        return {"input": input, **model_kwargs}

def benchmark_generator_get_prompt():
    template = "Template with many variables: " + " ".join([f"{{{{ var_{i} }}}}" for i in range(100)])
    prompt_kwargs = {f"var_{i}": f"value_{i}" for i in range(100)}

    generator = Generator(
        model_client=MockModelClient(),
        template=template,
        prompt_kwargs=prompt_kwargs
    )

    # Warm up
    generator.get_prompt()

    start_time = time.time()
    iterations = 100
    for _ in range(iterations):
        generator.get_prompt()
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average Generator.get_prompt time: {avg_time:.6f} seconds")

def benchmark_prompt_convert_kwargs(num_vars=1000):
    template = "Template"
    prompt_kwargs = {f"var_{i}": f"value_{i}" for i in range(num_vars)}
    prompt = Prompt(template=template, prompt_kwargs=prompt_kwargs)

    start_time = time.time()
    prompt._convert_prompt_kwargs_to_str(prompt_kwargs)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Prompt._convert_prompt_kwargs_to_str time for {num_vars} vars: {elapsed:.6f} seconds")
    return elapsed

if __name__ == "__main__":
    benchmark_generator_get_prompt()
    t1 = benchmark_prompt_convert_kwargs(1000)
    t2 = benchmark_prompt_convert_kwargs(2000)
    print(f"Scaling factor (should be ~4 if O(N^2)): {t2/t1:.2f}")
