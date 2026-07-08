from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
import re

app = FastAPI(
    title="Team Task Manager API",
    description="Mini Project - Hệ thống API Quản lý công việc nhóm",
    version="1.0"
)

# ======================================================
# DATABASE (In-memory)
# ======================================================

tasks_db = [
    {
        "id": 1,
        "title": "Thiet ke database Shop AI",
        "description": "Xay dung bang va toi uu index",
        "assignee": "QuyDev",
        "priority": 1,
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z",
        "internal_notes": "Chi Admin xem"
    },
    {
        "id": 2,
        "title": "Code bo API Authen",
        "description": "Trien khai filter verify JWT token",
        "assignee": "FixerQ",
        "priority": 2,
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z",
        "internal_notes": "Da kiem thu"
    }
]

# ======================================================
# SCHEMA
# ======================================================

class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=2)
    priority: int = Field(..., ge=1, le=5)


class TaskUpdateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=2)
    priority: int = Field(..., ge=1, le=5)
    status: str


class TaskStatusUpdateSchema(BaseModel):
    status: str


# Response Public (Không trả internal_notes)

class TaskPublicResponse(BaseModel):
    id: int
    title: str
    description: str
    assignee: str
    priority: int
    status: str
    created_at: str


# Unified Envelope

class ApiResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any]
    error: Optional[str]
    timestamp: str
    path: str


# ======================================================
# RESPONSE HELPER
# ======================================================

def create_response(
    status_code: int,
    message: str,
    data,
    error,
    path
):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "path": path
    }


# ======================================================
# REQUEST VALIDATION HANDLER
# ======================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=422,
        content=create_response(
            422,
            "Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",
            None,
            "ERR-VAL-422: Validation error at Request Body fields constraint layout.",
            request.url.path
        )
    )


# ======================================================
# HTTP EXCEPTION HANDLER
# ======================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    if isinstance(exc.detail, dict):

        return JSONResponse(
            status_code=exc.status_code,
            content=create_response(
                exc.status_code,
                exc.detail["message"],
                None,
                exc.detail["error"],
                request.url.path
            )
        )

    return JSONResponse(
        status_code=exc.status_code,
        content=create_response(
            exc.status_code,
            str(exc.detail),
            None,
            str(exc.detail),
            request.url.path
        )
    )


# ======================================================
# GLOBAL EXCEPTION HANDLER
# ======================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content=create_response(
            500,
            "Lỗi hệ thống!",
            None,
            "ERR-500: Internal Server Error.",
            request.url.path
        )
    )


# ======================================================
# BUSINESS FUNCTION
# ======================================================

def calculate_team_metrics():

    total_tasks = len(tasks_db)

    completed_tasks = 0

    for task in tasks_db:
        if task["status"] == "done":
            completed_tasks += 1

    if total_tasks == 0:
        completion_rate = 0
    else:
        completion_rate = round((completed_tasks / total_tasks) * 100, 2)

    return (
        total_tasks,
        completed_tasks,
        completion_rate
    )
    
    
    
# ======================================================
# GET ALL TASKS
# ======================================================

@app.get("/tasks")
def get_all_tasks():

    data = []

    for task in tasks_db:
        public_task = TaskPublicResponse(
            id=task["id"],
            title=task["title"],
            description=task["description"],
            assignee=task["assignee"],
            priority=task["priority"],
            status=task["status"],
            created_at=task["created_at"]
        )

        data.append(public_task.dict())

    return create_response(
        200,
        "Lấy danh sách công việc thành công!",
        data,
        None,
        "/tasks"
    )


# ======================================================
# SEARCH TASKS
# (Phải đặt trước /tasks/{task_id})
# ======================================================

@app.get("/tasks/search")
def search_tasks(
    keyword: Optional[str] = None,
    status: Optional[str] = None
):

    result = []

    for task in tasks_db:

        match = True

        if keyword:

            pattern = re.compile(keyword, re.IGNORECASE)

            if not (
                pattern.search(task["title"])
                or pattern.search(task["assignee"])
            ):
                match = False

        if status:

            if task["status"].lower() != status.lower():
                match = False

        if match:

            public_task = TaskPublicResponse(
                id=task["id"],
                title=task["title"],
                description=task["description"],
                assignee=task["assignee"],
                priority=task["priority"],
                status=task["status"],
                created_at=task["created_at"]
            )

            result.append(public_task.dict())

    return create_response(
        200,
        "Tìm kiếm công việc thành công!",
        {
            "total": len(result),
            "tasks": result
        },
        None,
        "/tasks/search"
    )


# ======================================================
# GET TASK DETAIL
# ======================================================

@app.get("/tasks/{task_id}")
def get_task_detail(task_id: int):

    for task in tasks_db:

        if task["id"] == task_id:

            public_task = TaskPublicResponse(
                id=task["id"],
                title=task["title"],
                description=task["description"],
                assignee=task["assignee"],
                priority=task["priority"],
                status=task["status"],
                created_at=task["created_at"]
            )

            return create_response(
                200,
                "Lấy chi tiết công việc thành công!",
                public_task.dict(),
                None,
                f"/tasks/{task_id}"
            )

    raise HTTPException(
        status_code=404,
        detail={
            "message": "Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            "error": "ERR-TASK-04: Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope."
        }
    )


# ======================================================
# CREATE TASK
# ======================================================

@app.post("/tasks")
def create_task(task: TaskCreateSchema):

    # Kiểm tra trùng title

    for item in tasks_db:

        if item["title"].lower() == task.title.lower():

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                    "error": "ERR-TASK-01: Task conflict: Title field values duplicates an existing record in the temporary database storage."
                }
            )

    new_id = 1

    if len(tasks_db) > 0:
        new_id = tasks_db[-1]["id"] + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "description": task.description,
        "assignee": task.assignee,
        "priority": task.priority,
        "status": "todo",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "internal_notes": ""
    }

    tasks_db.append(new_task)

    public_task = TaskPublicResponse(
        id=new_task["id"],
        title=new_task["title"],
        description=new_task["description"],
        assignee=new_task["assignee"],
        priority=new_task["priority"],
        status=new_task["status"],
        created_at=new_task["created_at"]
    )

    return create_response(
        201,
        "Tạo mới công việc nhóm thành công!",
        public_task.dict(),
        None,
        "/tasks"
    )
    
    # ======================================================
# UPDATE TASK
# ======================================================

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdateSchema):

    valid_status = [
        "todo",
        "in_progress",
        "done"
    ]

    if task.status not in valid_status:

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Lỗi: Trạng thái công việc cập nhật không đúng quy định!",
                "error": "ERR-TASK-03: Business logic error: Invalid task status value. Allowed enumerated selection list: ['todo', 'in_progress', 'done']."
            }
        )

    for item in tasks_db:

        if item["id"] == task_id:

            item["title"] = task.title
            item["description"] = task.description
            item["assignee"] = task.assignee
            item["priority"] = task.priority
            item["status"] = task.status

            public_task = TaskPublicResponse(
                id=item["id"],
                title=item["title"],
                description=item["description"],
                assignee=item["assignee"],
                priority=item["priority"],
                status=item["status"],
                created_at=item["created_at"]
            )

            return create_response(
                200,
                "Cập nhật công việc thành công!",
                public_task.dict(),
                None,
                f"/tasks/{task_id}"
            )

    raise HTTPException(
        status_code=404,
        detail={
            "message": "Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            "error": "ERR-TASK-04: Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope."
        }
    )


# ======================================================
# DELETE TASK
# ======================================================

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for index in range(len(tasks_db)):

        if tasks_db[index]["id"] == task_id:

            tasks_db.pop(index)

            return

    raise HTTPException(
        status_code=404,
        detail={
            "message": "Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            "error": "ERR-TASK-04: Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope."
        }
    )


# ======================================================
# DASHBOARD ANALYTICS
# ======================================================

@app.get("/tasks/analytics/dashboard")
def dashboard():

    total_tasks, completed_tasks, completion_rate = calculate_team_metrics()

    data = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate
    }

    return create_response(
        200,
        "Thống kê Dashboard thành công!",
        data,
        None,
        "/tasks/analytics/dashboard"
    )