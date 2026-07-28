from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(
    title = "Task API",
    description = "A simple CRUD API using SQLite",
    version = "2.0"
)

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
    )
""")

conn.commit()

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
        sample_tasks = [
            ("Buy Milk", False),
            ("Read a Book", False),
            ("Go for a Walk", False),
        ]

        cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                sample_tasks
        )

        conn.commit()

class TaskCreate(BaseModel):
        title: str

class TaskUpdate(BaseModel):
        title: str
        done: bool

@app.get("/")
def root():
        return {"message": "Welcome to Task API"}

@app.get("/health")
def health():
        return{"status": "Healthy"}

@app.get("/tasks")
def get_tasks():

        cursor.execute("SELECT * FROM tasks")

        rows = cursor.fetchall()
        tasks = []

        for row in rows:
                tasks.append({
                        "id": row[0],
                        "title": row[1],
                        "done": bool(row[2])
                })
        
        return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):

        cursor.execute(
                "SELECT * FROM tasks WHERE id = ?",
                (task_id,),
        )

        row = cursor.fetchone()

        if row is None:
                raise HTTPException(
                    status_code = 404,
                    detail = "Task not found"
                )

        return {
                "id": row[0],
                "title": row[1],
                "done": bool(row[2])
        }