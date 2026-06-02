from pydantic import BaseModel

class ItemResponse(BaseModel):
    items_id: int
    q: str | None = None

class HelloResponse(BaseModel):
    hello: str

class LLMRequest(BaseModel):
    question: str