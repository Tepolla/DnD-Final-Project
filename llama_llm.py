from llama_cpp import Llama
from illm import ILLM

class LlamaLLM(ILLM):
    def __init__(self, model_path: str, n_ctx: int = 512):
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx)

    def generate(self, prompt: str) -> str:
        # Generate a response using the Llama model
        response = self.llm(prompt, max_tokens=128, stop=["\n"])
        # The response is a dict; extract the generated text
        return response["choices"][0]["text"].strip()
