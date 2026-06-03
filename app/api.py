from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.api_service import ApiService
from app.models.api_model import HelloResponse, LLMRequest
from app.models.llm_model import PromptTemplate
from app.services.llm_service import SmolLM, ConversationHistory, DataStats
from app.services.csv_service import CSVService, CSVMetadata, CSVStats
import logging

logger = logging.getLogger(__name__)
MAX_CSV_SIZE = 20 * 1024 * 1024  # 20MB

# Core api class
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
        
        @self.app.get("/data/stats", response_model=CSVStats)
        async def get_stats():
            return self.csv_service.get_stats()

        @self.app.post("/ai/ask")
        async def ask_llm(request: LLMRequest):
            history_runnable = self.history
            stats_runnable = DataStats(csv_service=self.csv_service)
            prompt = PromptTemplate(
                template_str="Based on the data you have, answer the question: {q}"
            )
            context = history_runnable.get_context()

            chain = history_runnable | stats_runnable | prompt | self.llm

            result = chain.invoke({"q": request.question, "context": context})
            answer = result["answer"]
            self.history.add_turn(request.question, answer)

            return answer
        
        @self.app.post("/data/upload_csv", response_model=CSVMetadata)
        async def upload_csv(file: UploadFile = File(...)):
            if file.size is not None and file.size > MAX_CSV_SIZE:
                logger.error("Uploaded CSV size exceeds max limit")
                raise HTTPException(status_code=413, detail="CSV size exceeds max limit")
            
            await self.csv_service.parse_csv(file)
            return self.csv_service.get_metadata()

# Expose the FastAPI
api = MyAPI()
app = api.app
