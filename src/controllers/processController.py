from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models import ProcessingEnum


class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extention(self, file_id: str) -> str:
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        file_ext = self.get_file_extention(file_id=file_id)

        if file_ext in ['.txt', '.md']:
            return TextLoader(os.path.join(self.project_path, file_id))
        elif file_ext in ['.pdf']:
            return PyMuPDFLoader(os.path.join(self.project_path, file_id))
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
