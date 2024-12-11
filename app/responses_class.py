from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    sas_url: str
