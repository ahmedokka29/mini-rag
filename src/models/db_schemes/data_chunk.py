from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId


class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_text: str = Field(..., min_length=1,
                            description="Text content of the data chunk")
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0,
                             description="Order of the chunk within the project")
    chunk_project_id: ObjectId

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "keys": [
                    ("chunk_project_id", 1)
                ],
                "name": "chunk_project_id_index_1",
                "options": {"unique": False}
            }
        ]
