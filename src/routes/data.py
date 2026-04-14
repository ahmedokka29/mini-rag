from models import ResponseStatus
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
import os
from controllers import DataController, ProjectController, ProcessController
import aiofiles  # type: ignore
import logging
from .schemes.data import ProcessRequest
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
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    if file.filename is not None:
        file_path, file_id = data_controller.generate_unique_filename(
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
        content={"message": ResponseStatus.FILE_UPLOAD_SUCCESS.value,
                 "file_id": file_id
                 }
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunck_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)
    file_chuncks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunck_size,
        overlap_size=overlap_size
    )

    if file_chuncks is None or len(file_chuncks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseStatus.PROCESSING_FAILED.value}
        )

    return file_chuncks
