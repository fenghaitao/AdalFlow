import time
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient
from adalflow.core.prompt_builder import Prompt
from typing import Any, Dict, Optional

class MockModelClient(ModelClient):
    def call(self, api_kwargs: Dict, model_type: Any) -> str:
        return "mock response"

    def parse_chat_completion(self, completion: Any) -> Any:
        from adalflow.core.types import GeneratorOutput
        return GeneratorOutput(raw_response=completion)

    def convert_inputs_to_api_kwargs(self, input: str, model_kwargs: Dict, model_type: Any) -> Dict:
        return {"input": input, **model_kwargs}

class OldGenerator(Generator):
    def get_prompt(self, **kwargs) -> str:
        prompt = Prompt(template=self.template, prompt_kwargs=self.prompt_kwargs)
        return prompt.call(**kwargs)

    def _pre_call(self, prompt_kwargs: Dict, model_kwargs: Dict) -> Dict[str, Any]:
        prompt_str = self.get_prompt(**prompt_kwargs)
        composed_model_kwargs = self._compose_model_kwargs(**model_kwargs)
        api_kwargs = self.model_client.convert_inputs_to_api_kwargs(
            input=prompt_str,
            model_kwargs=composed_model_kwargs,
            model_type=self.model_type,
        )
        return api_kwargs

    def call(self, prompt_kwargs={}, model_kwargs={}, use_cache=None, id=None):
        prompt_str = self.get_prompt(**prompt_kwargs) # get_prompt call 1
        api_kwargs = self._pre_call(prompt_kwargs, model_kwargs) # get_prompt call 2 (via _pre_call)
        completion = self._model_client_call(api_kwargs=api_kwargs, use_cache=False)
        output = self._post_call(completion)
        return output

def benchmark():
    # Long template with very few variables
    template_str = "System: You are a helpful assistant.\n" + "Literal text " * 10000 + "\nInput: {{input_str}}"
    prompt_kwargs = {"input_str": "test"}

    iterations = 100

    old_gen = OldGenerator(
        model_client=MockModelClient(),
        model_kwargs={"model": "mock-model"},
        template=template_str,
        prompt_kwargs=prompt_kwargs,
        use_cache=False
    )

    new_gen = Generator(
        model_client=MockModelClient(),
        model_kwargs={"model": "mock-model"},
        template=template_str,
        prompt_kwargs=prompt_kwargs,
        use_cache=False
    )

    # Warm up
    old_gen.call()
    new_gen.call()

    print("--- get_prompt ---")
    start_time = time.time()
    for i in range(iterations):
        old_gen.get_prompt()
    print(f"OLD: {(time.time() - start_time) / iterations * 1000:.4f} ms")

    start_time = time.time()
    for i in range(iterations):
        new_gen.get_prompt()
    print(f"NEW: {(time.time() - start_time) / iterations * 1000:.4f} ms")

    print("\n--- call ---")
    start_time = time.time()
    for i in range(iterations):
        old_gen.call()
    print(f"OLD: {(time.time() - start_time) / iterations * 1000:.4f} ms")

    start_time = time.time()
    for i in range(iterations):
        new_gen.call()
    print(f"NEW: {(time.time() - start_time) / iterations * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
