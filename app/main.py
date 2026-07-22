"""
A tiny Task Manager API — built for learning Python + Git + Docker.

Endpoints:
  GET    /tasks         -> list all tasks
  POST   /tasks          -> create a task
  GET    /tasks/{id}     -> get one task
  PUT    /tasks/{id}     -> update a task
  DELETE /tasks/{id}     -> delete a task
  GET    /health         -> health check (useful for Docker healthchecks)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI(title="Task API", version="1.0.0")

# In-memory "database" - resets every time the container restarts.
# Swap this for a real database (Postgres, SQLite, etc.) once you're
# comfortable with the basics.
tasks: dict[str, dict] = {}


class TaskIn(BaseModel):
    title: str
    done: bool = False


class TaskOut(TaskIn):
    id: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks():
    return list(tasks.values())


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskIn):
    task_id = str(uuid4())
    record = {"id": task_id, **task.model_dump()}
    tasks[task_id] = record
    return record


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: str):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: str, task: TaskIn):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    record = {"id": task_id, **task.model_dump()}
    tasks[task_id] = record
    return record


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
