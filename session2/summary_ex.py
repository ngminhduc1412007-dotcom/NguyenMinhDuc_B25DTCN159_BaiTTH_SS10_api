from fastapi import FastAPI

app = FastAPI()

courses = [
    {
        "id": 1,
        "code": "PY101",
        "name": "Python Basic",
        "level": "beginner",
        "price": 1500000
    },
    {
        "id": 2,
        "code": "FA101",
        "name": "FastAPI Basic",
        "level": "beginner",
        "price": 2000000
    }
]

@app.get("/health")
def get_health():
    return {
        "message": "API is running"
    }
    
@app.get("/courses")
def get_courses():
    return courses

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    if course_id <= 0:
        return{
            "message": "course_id must be greater than 0"
        }

    for course in courses:
        if course["id"] == course_id:
            return course

    return{
        "message": "Course not found"
    }