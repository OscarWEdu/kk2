from models.api_model import HelloResponse, ItemResponse
from functools import wraps

def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"done {func.__name__}")
        return result
    return wrapper

class ApiService:
    @log_calls
    def get_root(self) -> HelloResponse:
        return HelloResponse(hello="world")

    @log_calls
    def get_item(self, item_id: int, q: str | None = None) -> ItemResponse:
        return ItemResponse(items_id=item_id, q=q)
