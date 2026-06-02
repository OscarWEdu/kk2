from pydantic import BaseModel
from typing import Any


class PromptTemplate(BaseModel):
    template_str: str

    def format(self, **kwargs):
        return self.template_str.format(**kwargs)

    def __or__(self, other):
        from services.llm_service import SmolLM  # avoid circular import
        if isinstance(other, SmolLM):
            return LLMChain(prompt_template=self, llm=other)
        raise TypeError("Right-hand side must be a SmolLM instance")


class LLMChain(BaseModel):
    prompt_template: PromptTemplate
    llm: Any  # SmolLM instance (non-serializable)

    model_config = {
        "arbitrary_types_allowed": True
    }

    def invoke(self, **kwargs):
        formatted_prompt = self.prompt_template.format(**kwargs)
        return self.llm.invoke(formatted_prompt)
