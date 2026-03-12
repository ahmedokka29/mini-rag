from fastapi import FastAPI, APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
import os
from controllers import DataController, ProjectController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=['api_v1', 'data']
)


@data_router.post("/upload/{project_id}")
def upload_data(project_id: str, file: UploadFile,
                app_settings: Settings = Depends(get_settings)):

    # Validate file properties
    is_valid, result_signal = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": result_signal}
        )

    # Save the file to the specified location
    project_dir_oath = ProjectController().get_project_path(project_id=project_id)
    file_path = os.path.join(project_dir_oath, file.filename)
