from models.api_model import HelloResponse
from functools import wraps

# Decorator method for logging
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
        return HelloResponse(hello="Viable endpoints are:\nPOST /data/upload\nGET /data/stats\nPOST /ai/askGET /health")

