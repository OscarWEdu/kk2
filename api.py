from fastapi import FastAPI
from services.api_service import ApiService
from models.api_model import HelloResponse, ItemResponse

class MyAPI:
    def __init__(self):
        self.app = FastAPI()
        self.service = ApiService()
        self._add_routes()

    def _add_routes(self):
        @self.app.get("/", response_model=HelloResponse)
        async def read_root():
            return self.service.get_root()

        @self.app.get("/items/{item_id}", response_model=ItemResponse)
        async def read_items(item_id: int, q: str | None = None):
            return self.service.get_item(item_id, q)


# Expose the FastAPI
api = MyAPI()
app = api.app
