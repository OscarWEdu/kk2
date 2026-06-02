# Run with "uv run fastapi dev main.py"
from fastapi import FastAPI
from functools import wraps
from utils.config import config

# Currying function
def log_calls(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        result = await func(*args, **kwargs)
        print(f"done {func.__name__}")
        return result
    return wrapper


class MyAPI:
    def __init__(self):
        self.app = FastAPI()
        self._add_routes()

    def _add_routes(self):
        @self.app.get("/")
        @log_calls
        async def read_root():
            return {"hello": "world"}

        @self.app.get("/items/{item_id}")
        @log_calls
        async def read_items(item_id: int, q: str | None = None):
            return {"items_id": item_id, "q": q}


# Expose the FastAPI
api = MyAPI()
app = api.app
