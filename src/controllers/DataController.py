from .BaseController import BaseController
from fastapi import UploadFile, File


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # Convert MB to Bytes

    def validate_uploaded_file(self, file: UploadFile):
        # Implement validation logic for the uploaded file
        # For example, check file type, size, etc.
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False

        return True
