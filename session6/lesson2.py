from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class AddStudent(BaseModel):
    id: int
    code: str
    name: str
    email: str
    age: int
    
app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

@app.post("/students")
def create_student(student: AddStudent):
    for s in students:
        if s["id"] == student.id:
            return {
                "message": "The id already exists"
            }

    for s in students:
        if s["code"].upper() == student.code.upper():
            return {
                "message": "The code already exists"
            }

    for s in students:
        if s["email"].lower() == student.email.lower():
            return {
                "message": "The email already exists"
            }

    if student.name.strip() == "":
        return {
            "message": "Name cannot be empty"
        }

    if student.age <= 0:
        return {
            "message": "Age must be greater than 0"
        }

    new_student = {
        "id": student.id,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }
    students.append(new_student)
    return {
        "message": "Create successfully",
        "data": new_student
    }

@app.get("/students")
def get_student():
    return {
        "message": "All student in list",
        "data": students
    }

@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return {
                "message": "Student found",
                "data": student
            }

    return {
        "message": "Student not found",
        "data": None
    }

@app.put("/students/{student_id}")
def update_student(student_id: int, student: AddStudent):
    target_student = None
    for s in students:
        if s["id"] == student_id:
            target_student = s
            break

    if target_student is None:
        return {
            "message": "Student not found"
        }

    for s in students:
        if s["id"] == student.id and s != target_student:
            return {
                "message": "The id already exists"
            }

    for s in students:
        if s["code"].upper() == student.code.upper() and s != target_student:
            return {
                "message": "The code already exists"
            }

    for s in students:
        if s["email"].lower() == student.email.lower() and s != target_student:
            return {
                "message": "The email already exists"
            }

    if student.name.strip() == "":
        return {
            "message": "Name cannot be empty"
        }

    if student.age <= 0:
        return {
            "message": "Age must be greater than 0"
        }

    target_student["id"] = student.id
    target_student["code"] = student.code
    target_student["name"] = student.name
    target_student["email"] = student.email
    target_student["age"] = student.age
    return {
        "message": "Update successfully",
        "data": target_student
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {
                "message": "Delete successfully",
                "data": student
            }

    return {
        "message": "Student not found",
        "data": None
    }
    
@app.get("/students/search")
def search_students(keyword: Optional[str] = None, min_age: Optional[int] = None, max_age: Optional[int] = None):
    result = students
    if keyword:
        keyword = keyword.lower()
        result = [student for student in result if keyword in student["name"].lower() or keyword in student["code"].lower() or keyword in student["email"].lower()]

    if min_age is not None:
        result = [student for student in result if student["age"] >= min_age]

    if max_age is not None:
        result = [student for student in result if student["age"] <= max_age]
    return {
        "message": "Get students successfully",
        "data": result
    }
