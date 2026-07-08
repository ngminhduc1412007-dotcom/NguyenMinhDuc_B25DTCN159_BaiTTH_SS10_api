from fastapi import FastAPI
from typing import Optional
app = FastAPI()

courses = [
    {
        "id": 1,
        "name": "Python Basic",
        "category": "backend",
        "price": 3000000,
        "mode": "online"
    },
    {
        "id": 2,
        "name": "Java Web",
        "category": "backend",
        "price": 5000000,
        "mode": "offline"
    },
    {
        "id": 3,
        "name": "Web Frontend",
        "category": "frontend",
        "price": 4000000,
        "mode": "online"
    }
]

@app.get("/courses")
def get_courses():
    return {
        "message": "Lấy danh sách khóa học thành công",
        "data": courses
    }
    
@app.get("/courses/search")
def search_courses(mode: Optional[str] = None, category: Optional[str] = None):
    filter_courses = courses
    if mode:
        filter_courses = [course for course in filter_courses if course["mode"].lower() == mode.lower()]
        
    if category:
        filter_courses = [course for course in filter_courses if course["category"].lower() == category.lower()]
        
    return {
        "message": "Lấy danh sách khóa học thành công",
        "data": filter_courses
    }
    
@app.get("/courses/{course_id}")
def get_course_by_id(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return {
                "message": "Tìm thấy khóa học",
                "data": course
            }
    
    return {
        "message": "Không tìm thấy khóa học",
        "data": None
    }