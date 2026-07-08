from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class AddCourses(BaseModel):
    id: int
    code: str
    name: str
    duration: int
    fee: int

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

@app.post("/courses")
def create_courses(course: AddCourses):
    for c in courses:
        if c["id"] == course.id:
            return {
                "message": "The id already exists"
            }

    for c in courses:
        if c["code"].upper() == course.code.upper():
            return {
                "message": "The code already exists"
            }

    if course.name.strip() == "":
        return {
            "message": "Name cannot be empty"
        }

    if course.duration <= 0:
        return {
            "message": "Duration must be greater than 0"
        }

    if course.fee < 0:
        return {
            "message": "Fee must be greater than or equal to 0"
        }

    new_course = {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }
    courses.append(new_course)
    return {
        "message": "Enroll successfully",
        "data": new_course
    }

@app.get("/courses")
def get_courses():
    return {
        "message": "All courses in list",
        "data": courses
    }

@app.get("/courses/{course_id}")
def get_course_by_id(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return {
                "message": "Course found",
                "data": course
            }

    return {
        "message": "Course not found",
        "data": None
    }

@app.put("/courses/{course_id}")
def update_courses(course_id: int, course: AddCourses):
    target_course = None
    for c in courses:
        if c["id"] == course_id:
            target_course = c
            break

    if target_course is None:
        return {
            "message": "Course not found"
        }

    for c in courses:
        if c["id"] == course.id and c != target_course:
            return {
                "message": "The id already exists"
            }

    for c in courses:
        if c["code"].upper() == course.code.upper() and c != target_course:
            return {
                "message": "The code already exists"
            }

    if course.name.strip() == "":
        return {
            "message": "Name cannot be empty"
        }

    if course.duration <= 0:
        return {
            "message": "Duration must be greater than 0"
        }

    if course.fee < 0:
        return {
            "message": "Fee must be greater than or equal to 0"
        }

    target_course["id"] = course.id
    target_course["code"] = course.code
    target_course["name"] = course.name
    target_course["duration"] = course.duration
    target_course["fee"] = course.fee
    return {
        "message": "Update successfully",
        "data": target_course
    }

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)
            return {
                "message": "Delete successfully",
                "data": course
            }

    return {
        "message": "Course not found",
        "data": None
    }

@app.get("/courses/search")
def search_courses(keyword: Optional[str] = None, min_fee: Optional[int] = None, max_fee: Optional[int] = None):
    result = courses
    if keyword:
        keyword = keyword.lower()
        result = [course for course in result if keyword in course["name"].lower() or keyword in course["code"].lower()]

    if min_fee is not None:
        result = [course for course in result if course["fee"] >= min_fee]

    if max_fee is not None:
        result = [course for course in result if course["fee"] <= max_fee]

    return {
        "message": "Search successfully",
        "data": result
    }