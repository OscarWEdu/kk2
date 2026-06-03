from pydantic import BaseModel
from typing import Any, Dict

class Runnable(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    def invoke(self, input: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def __or__(self, other: "Runnable"):
        return RunnableSequence(first=self, second=other)

class RunnableSequence(Runnable):
    first: Runnable
    second: Runnable

    def invoke(self, input: Dict[str, Any]) -> Dict[str, Any]:
        out1 = self.first.invoke(input)
        out2 = self.second.invoke(out1)
        return out2

class PromptTemplate(Runnable):
    template_str: str

    def invoke(self, input: Dict[str, Any]) -> Dict[str, Any]:
        formatted_str = self.template_str.format(**input)
        return {"prompt": formatted_str, **input}


class HistoryPair(BaseModel):
    user: str
    ai: str