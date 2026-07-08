from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class CreateStudent(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=20)
    age: Optional[int] = 18
    email: EmailStr[str]

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A", "age": 19},
    {"id": 2, "name": "Le Thi B", "age": 20}
]

# api co chuc nang them sinh vien 
@app.post("/student")
def create_student(new_student: CreateStudent):
    return {
        "data": new_student
    }