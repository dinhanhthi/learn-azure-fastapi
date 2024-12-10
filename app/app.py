from typing import Union

from fastapi import FastAPI

from app.helpers import get_env_name

app = FastAPI()


@app.get("/")
def read_root():
    env_name = get_env_name()
    return {"Hello": f"World from env_name {env_name}!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/health-check")
def health_check():
    return {"status": "ok"}