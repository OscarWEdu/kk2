from fastapi import FastAPI, UploadFile, File
from services.api_service import ApiService
from models.api_model import HelloResponse, LLMRequest
from models.llm_model import PromptTemplate
from services.llm_service import SmolLM, ConversationHistory
from services.csv_service import CSVService

class MyAPI:
    def __init__(self):
        self.app = FastAPI()
        self.service = ApiService()
        self.llm = SmolLM()
        self.history = ConversationHistory()
        self.csv_service = CSVService()
        self._add_routes()

    def _add_routes(self):
        @self.app.get("/", response_model=HelloResponse)
        async def read_root():
            return self.service.get_root()
        
        @self.app.get("/health")
        async def read_health():
            return "ok"

        @self.app.post("/ai/ask")
        async def ask_llm(request: LLMRequest):
            prompt = PromptTemplate(
                template_str="Based on the data you have, answer the question: {q}"
            )

            context = self.history.get_context()

            chain = prompt | self.llm

            result = chain.invoke({"q": request.question, "context": context})
            answer = result["answer"]
            self.history.add_turn(request.question, answer)

            return answer
        
        @self.app.post("/data/upload_csv")
        async def upload_csv(file: UploadFile = File(...)):
            parsed = await self.csv_service.parse_csv(file)

            return parsed

# Expose the FastAPI
api = MyAPI()
app = api.app
