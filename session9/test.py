from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from fastapi.responses import JSONResponse

class CreateCourses(BaseModel):
    id: int
    course_name: str
    duration_hours: int
    price: int
    status: str
    created_at: str
    
class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any]
    error: Optional[str]
    timestamp: str
    path: str

courses_db = [
    {"id": 1, "course_name": "FastAPI Masterclass", "duration_hours": 32, "price": 1500000, "status": "active", "created_at": "2026-07-01T02:00:00Z"},
    {"id": 2, "course_name": "NextJS Next-Level", "duration_hours": 45, "price": 1800000, "status": "active", "created_at": "2026-07-01T03:15:00Z"}
]

app = FastAPI()

def create_response(request: Request, status_code: int, message: str, data = None, error = None):
    return BaseResponse(
        status_code=status_code,
        message=message,
        data=data,
        error=error,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.get("/courses")
def get_courses(request: BaseResponse):
    return create_response(request, status.HTTP_200_OK, "Success!", courses_db)

@app.post("/courses")
def create_courses(new_courses: CreateCourses, request: BaseModel):
    course = new_courses.model_dump()
    courses_db.append(course)
    return create_response(request, status.HTTP_201_CREATED, "Success!", courses_db)

@app.delete("/courses/{course_id}")
def delete_courses(request: Request, course_id: int):
    for c in courses_db:
        if c["id"] == course_id:
            courses_db.remove(c)
            return create_response(request, status.HTTP_200_OK, "Success!", c)
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")

@app.exception_handler(Exception)
def global_exception_handler(
    request: Request,
    exc: Exception
):
    response = create_response(request, status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed", errors= str(exc))
    return JSONResponse(
        content=response.model_dump(),
        status_code=response.status_code
    )
    
    