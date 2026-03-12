from fastapi import FastAPI, APIRouter, Depends, File, UploadFile
from helpers.config import get_settings, Settings
import os
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=['api_v1', 'data']
)


@data_router.post("/upload/{project_id}")
def upload_data(project_id: str, file: UploadFile,
                app_settings: Settings = Depends(get_settings)):

    # Validate file properties
    is_valid = DataController().validate_uploaded_file(file=file)

    return is_valid
