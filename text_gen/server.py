from ray import serve
from starlette.requests import Request
from typing import List
from transformers import pipeline

@serve.deployment
class Text2Text:
    def __init__(self) -> None:
        # https://huggingface.co/tasks/text-generation
        self.model = pipeline('text2text-generation', model='gpt2')

    def ask(self, prompt) -> List[str]:
        predictions = self.model(prompt, max_length = 50, num_return_sequences=1)
        return [str(sequence["generated_text"]) for sequence in predictions]

    async def __call__(self, request: Request) -> List[str]:
        return self.ask(request.query_params["question"])

deployment = Text2Text.bind()

