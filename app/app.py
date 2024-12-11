from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from app.helpers import get_env_name, remove_422, remove_422s
from app.main_functions import upload_azure_storage_account
from app.responses_class import UploadResponse

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    env_name = get_env_name()
    return {"Hello": f"World from env_name {env_name}!"}


@app.post("/upload")
@remove_422
async def upload(file: UploadFile = File(...)) -> UploadResponse:
    sas_url = await upload_azure_storage_account(file)
    return {"filename": file.filename, "sas_url": sas_url}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/health-check")
def health_check():
    """Health check endpoint, used by Azure App Service"""
    return {"status": "ok"}

remove_422s(app)