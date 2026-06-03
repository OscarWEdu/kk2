from transformers import pipeline
from typing import List
from app.models.llm_model import HistoryPair, Runnable
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

# Class handling llm conversation memory
class ConversationHistory(Runnable):
    history: List[HistoryPair] = []

    def add_turn(self, user: str, ai: str):
        self.history.append(HistoryPair(user=user, ai=ai))

    def get_context(self) -> str:
        if not self.history:
            return ""
        return "\n".join(
            f"User: {turn.user}\nLLM: {turn.ai}"
            for turn in self.history
        )

    def invoke(self, input: Dict[str, Any]) -> Dict[str, Any]:
        context = self.get_context()
        return {"context": context, **input}
    
class DataStats(Runnable):
    csv_service: Any

    def invoke(self, input: Dict[str, Any]) -> Dict[str, Any]:
        context = input.get("context", "")
        if self.csv_service.df is None:
            return input
        
        stats_text = self.csv_service.get_formatted_stats()
        new_context = f"{context}\n\nDataset statistics:\n{stats_text}"
        return {**input, "context": new_context}

# Core llm class, hardcoded to use the provided llm model
class SmolLM(Runnable):
    pipe: Any = None

    def __init__(self, model_name="HuggingFaceTB/SmolLM2-135M-Instruct"): #recommended model for release HuggingFaceTB/SmolLM-1.7B-Instruct
        super().__init__()
        from transformers import pipeline
        self.pipe = pipeline("text-generation", model_name)

    # Constructs the llm prompt and uses built in pipeline method to generate a response
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
        logger.info("LLM Output: %s", output)
        answer = output[0]["generated_text"][-1]["content"]

        return {"answer": answer, **input}


