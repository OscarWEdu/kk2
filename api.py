from fastapi import FastAPI
from services.api_service import ApiService
from models.api_model import HelloResponse, ItemResponse, LLMRequest
from models.llm_model import PromptTemplate
from services.llm_service import SmolLM

class MyAPI:
    def __init__(self):
        self.app = FastAPI()
        self.service = ApiService()
        self.llm = SmolLM()
        self._add_routes()

    def _add_routes(self):
        @self.app.get("/", response_model=HelloResponse)
        async def read_root():
            return self.service.get_root()

        @self.app.get("/items/{item_id}", response_model=ItemResponse)
        async def read_items(item_id: int, q: str | None = None):
            return self.service.get_item(item_id, q)

        @self.app.post("/llm/ask")
        async def ask_llm(request: LLMRequest):
            prompt = PromptTemplate(
                template_str="Based on the data you have, answer the question: {q}"
            )
            chain = prompt | self.llm
            result = chain.invoke(q=request.question)
            return {"response": result}


# Expose the FastAPI
api = MyAPI()
app = api.app
