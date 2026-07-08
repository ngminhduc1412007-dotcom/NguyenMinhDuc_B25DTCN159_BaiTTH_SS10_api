from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]
class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int
@app.post("/enrollments")
def create_enrollment(enrollment: EnrollmentCreate):
    for e in enrollments:
        if (e["student_id"].strip().upper() == enrollment.student_id.strip().upper()) and (e["course_id"] == enrollment.course_id):
            return {
                "message": "Hoc vien da dang ky khoa hoc nay",
                "data": None
            }
            
    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }
    enrollments.append(new_enrollment)
    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }