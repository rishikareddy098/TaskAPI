from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from postgres_repository import PostgresTaskRepository


app = FastAPI(
    title="Task API",
    description="A simple CRUD API using PostgreSQL",
    version="3.0"
)


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


repository = PostgresTaskRepository(DATABASE_URL)


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


@app.get("/", summary="API Information")
def root():
    return {
        "name": "Task API",
        "version": "3.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Health Check")
def health():
    return {
        "status": "OK"
    }


@app.get("/tasks", summary="Get All Tasks")
def get_tasks():
    return repository.get_tasks()


@app.get("/tasks/{task_id}", summary="Get Task by ID")
def get_task(task_id: int):

    task = repository.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found..!"
        )

    return task


@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    return repository.create_task(task.title)


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, updated_task: TaskUpdate):

    if not updated_task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty..!"
        )

    task = repository.update_task(
        task_id,
        updated_task.title,
        updated_task.done
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found..!"
        )

    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):

    deleted = repository.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found..!"
        )

    return