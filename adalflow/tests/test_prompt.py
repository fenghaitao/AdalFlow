import unittest
from jinja2 import Template
from adalflow.core.prompt_builder import Prompt
from adalflow.optim.parameter import Parameter, ParameterType


class TestPrompt(unittest.TestCase):
    def test_basic_prompt_rendering(self):
        template = "Hello {{ name }}!"
        prompt = Prompt(template=template)
        rendered = prompt.call(name="World")
        self.assertEqual(rendered, "Hello World!")

    def test_prompt_with_default_kwargs(self):
        template = "Task: {{ task }}, Input: {{ input }}"
        prompt = Prompt(template=template, prompt_kwargs={"task": "Summarize"})
        rendered = prompt.call(input="Text content")
        self.assertEqual(rendered, "Task: Summarize, Input: Text content")

    def test_parameter_in_prompt_kwargs(self):
        template = "Instruction: {{ instruction }}"
        param = Parameter(
            data="Be concise",
            role_desc="system instruction",
            param_type=ParameterType.PROMPT,
        )
        prompt = Prompt(template=template, prompt_kwargs={"instruction": param})
        rendered = prompt.call()
        self.assertEqual(rendered, "Instruction: Be concise")

    def test_nested_prompt_rendering(self):
        outer_template = "Header\n{{ inner_prompt }}\nFooter"
        inner_template = "Item: {{ item_name }}"

        inner = Prompt(template=inner_template)
        outer = Prompt(template=outer_template)

        rendered = outer.call(inner_prompt=inner, item_name="Widget")
        self.assertEqual(rendered, "Header\nItem: Widget\nFooter")

    def test_nested_jinja_template_rendering(self):
        outer_template = "Greeting: {{ sub_template }}"
        sub_tpl = Template("Hi {{ user }}")

        outer = Prompt(template=outer_template)
        rendered = outer.call(sub_template=sub_tpl, user="Alice")
        self.assertEqual(rendered, "Greeting: Hi Alice")

    def test_large_kwargs_performance_and_correctness(self):
        template = "Value: {{ key_0 }}"
        kwargs = {f"key_{i}": f"value_{i}" for i in range(200)}

        prompt = Prompt(template=template)
        rendered = prompt.call(**kwargs)
        self.assertEqual(rendered, "Value: value_0")

    def test_prompt_serialization(self):
        template = "Test {{ x }}"
        prompt = Prompt(template=template, prompt_kwargs={"x": "123"})
        data = prompt.to_dict()
        restored = Prompt.from_dict(data)
        self.assertEqual(restored.call(), "Test 123")


if __name__ == "__main__":
    unittest.main()
