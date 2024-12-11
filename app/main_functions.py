import os
from azure.storage.blob import (
    BlobServiceClient,
    BlobSasPermissions,
    generate_blob_sas
)
from fastapi import UploadFile
import datetime


async def upload_azure_storage_account(file: UploadFile):

    account_name = os.getenv('ACCOUNT_STORAGE_NAME')
    account_key = os.getenv('ACCOUNT_STORAGE_KEY')
    container_name = os.getenv('CONTAINER_NAME')
    blob_name = file.filename
    file_content = await file.read()

    # https://learn.microsoft.com/en-us/azure/storage/common/storage-account-sas-create-python
    blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key
    )
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(file_content, overwrite=True)

    start_time = datetime.datetime.now(datetime.timezone.utc)
    expiry_time = start_time + datetime.timedelta(days=1)

    sas_token = generate_blob_sas(
        account_name=blob_client.account_name,
        container_name=blob_client.container_name,
        blob_name=blob_client.blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry_time,
        start=start_time
    )

    sas_url = f"{blob_client.url}?{sas_token}"

    return sas_url
