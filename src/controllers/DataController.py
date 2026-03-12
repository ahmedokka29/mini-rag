import os

from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile, File
from models import ResponseStatus
import re


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # Convert MB to Bytes

    def validate_uploaded_file(self, file: UploadFile):
        # Implement validation logic for the uploaded file
        # For example, check file type, size, etc.
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseStatus.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False, ResponseStatus.FILE_SIZE_EXCEEDS_LIMIT.value

        return True, ResponseStatus.FILE_VALIDATED_SUCCESS.value

    def generate_unique_filename(self, original_filename: str, project_id: str):
        # Implement logic to generate a unique filename
        random_string = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_filename = self.get_clean_filename(filename=original_filename)

        new_file_path = os.path.join(
            project_path,
            f"{random_string}_{cleaned_filename}"
        )

        while os.path.exists(new_file_path):
            random_string = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                f"{random_string}_{cleaned_filename}"
            )

        return new_file_path

    def get_clean_filename(self, filename: str):
        # Remove any characters that are not alphanumeric, dots, or underscores
        cleaned_filename = re.sub(r'[^\w.-]', '_', filename.strip())

        # Replace spaces with underscores
        cleaned_filename = cleaned_filename.replace(' ', '_')
        return cleaned_filename
