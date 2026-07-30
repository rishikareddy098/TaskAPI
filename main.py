from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import conn, cursor

app = FastAPI(
    title = "Task API",
    description = "A simple CRUD API for manging tasks",
    version = "1.0"
)

tasks = [
    {"id": 1, "title" : "Study Python", "done" : False},
    {"id": 2, "title" : "Complete Assignment", "done" : False},
    {"id": 3, "title" : "Read a Book", "done" : True}
]

class TaskCreate(BaseModel):
    title : str

class TaskUpdate(BaseModel):
    title : str
    done : bool

@app.get("/", summary = "API Information")
def root():
    return {
        "name" : "Task API",
        "version" : "1.0",
        "endpoints" : ["/tasks"]
    }

@app.get("/health", summary = "Health Check")
def health():
    return {
        "status" : "OK"
    }

@app.get("/tasks", summary = "Get All Tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", summary = "Get Task by ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(
        status_code = 404,
        detail = f"Task {task_id} not found..!"
    )

@app.post("/tasks", status_code = 201, summary = "Create a new task")
def create_task(task : TaskCreate):
    if not task.title.strip():
        raise HTTPException(
            status_code = 400,
            detail = "Title cannot be empty"
        )

    new_task = {
        "id" : len(tasks) + 1,
        "title" : task.title,
        "done" : False
    }

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{task_id}", summary = "Update a task")
def update_task(task_id: int, updated_task: TaskUpdate):

    if not updated_task.title.strip():
        raise HTTPException(
            status_code = 400,
            detail = "Title cannot be empty..!"
        )
    
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["done"] = updated_task.done
            return task
        
    raise HTTPException(
        status_code = 404,
        detail = f"Task {task_id} not found..!"
    )

@app.delete("/tasks/{task_id}", status_code = 204, summary = "Delete a task")
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code = 404,
        detail = f"Task {task_id} not found..!"
    )