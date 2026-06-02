from transformers import pipeline
from models.llm_model import HistoryPair


class SmolLM:
    def __init__(self, model_name="HuggingFaceTB/SmolLM-135M-Instruct"):
        print("Loading model...")
        self.pipe = pipeline("text-generation", model_name)
        print("Model loaded.")

    def invoke(self, prompt: str):
        messages = [
            {"role": "system", "content": "You are a bratty AI tutor, which speaks in short sentences"},
            {"role": "user", "content": prompt}
        ]

        output = self.pipe(messages, max_new_tokens=150)
        return output[0]["generated_text"][-1]["content"]
