from pydantic import BaseModel

class HelloResponse(BaseModel):
    hello: str

class LLMRequest(BaseModel):
    question: str