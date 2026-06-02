from fastapi import FastAPI
from services.api_service import ApiService
from models.api_model import HelloResponse, ItemResponse, LLMRequest
from models.llm_model import PromptTemplate
from services.llm_service import SmolLM, ConversationHistory

class MyAPI:
    def __init__(self):
        self.app = FastAPI()
        self.service = ApiService()
        self.llm = SmolLM()
        self.history = ConversationHistory()
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
            context = self.history.get_context()

            chain = prompt | self.llm
            answer = chain.llm.invoke(prompt=prompt.format(q=request.question), context=context)

            self.history.add_turn(
                user=request.question,
                ai=answer
            )

            return answer


# Expose the FastAPI
api = MyAPI()
app = api.app
