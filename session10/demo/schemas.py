from pydantic import BaseModel
from datetime import datetime

class CreateClassroom(BaseModel):
    class_code: str
    name: str
    description: str
    created_at: datetime