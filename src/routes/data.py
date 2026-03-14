from models import ResponseStatus
from fastapi import FastAPI, APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
import os
from controllers import DataController, ProjectController
import aiofiles
import logging
logger = logging.getLogger('uvicorn.error')


data_router = APIRouter(
    prefix="/api/v1/data",
    tags=['api_v1', 'data']
)


@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):

    data_controller = DataController()
    # Validate file properties
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": result_signal}
        )

    # Save the file to the specified location
    project_dir_oath = ProjectController().get_project_path(project_id=project_id)
    if file.filename is not None:
        file_path = data_controller.generate_unique_filename(
            original_filename=file.filename,
            project_id=project_id
        )
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": ResponseStatus.FILE_UPLOAD_FAILURE.value}
        )
    return JSONResponse(

        content={"message": ResponseStatus.FILE_UPLOAD_SUCCESS.value}
    )
