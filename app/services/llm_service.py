from transformers import pipeline
from typing import List
from models.llm_model import HistoryPair, Runnable
from typing import Any, Dict

class ConversationHistory:
    def __init__(self):
        self.history: List[HistoryPair] = []

    def add_turn(self, user: str, ai: str):
        self.history.append(HistoryPair(user=user, ai=ai))

    def get_context(self) -> str:
        if not self.history:
            return ""

        return "\n".join(
            f"User: {turn.user}\nLLM: {turn.ai}"
            for turn in self.history
        )

class SmolLM(Runnable):
    pipe: Any = None

    def __init__(self, model_name="HuggingFaceTB/SmolLM-135M-Instruct"):
        super().__init__()
        from transformers import pipeline
        self.pipe = pipeline("text-generation", model_name)

    def invoke(self, input: Dict[str, Any]) -> Dict[str, Any]:
        prompt = input["prompt"]
        context = input.get("context", "")

        messages = [
            {"role": "system", "content": "You are a helpful AI statistician, which speaks in curt, short sentences"}
        ]

        if context:
            messages.append({"role": "system", "content": f"Conversation so far:\n{context}"})

        messages.append({"role": "user", "content": prompt})

        output = self.pipe(messages, max_new_tokens=150)
        answer = output[0]["generated_text"][-1]["content"]

        return {"answer": answer, **input}


