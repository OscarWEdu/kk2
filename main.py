#Run with "uv run fastapi dev main.py" 

from fastapi import FastAPI

app = FastAPI()

#Currying function
def log_calls(func):
    async def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        result = await func(*args, **kwargs)
        print(f"done {func.__name__}")
        return result
    return wrapper


@log_calls
@app.get("/")
async def read_root():
    return {"hello": "world"}
    
@log_calls
@app.get("/items/{item_id}")
async def read_items(item_id: int, q: str | None = None):
    return {"items_id": item_id, "q": q}
