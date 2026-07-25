from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import Base, engine, SessionLocal
from app.models import Task

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task API", version="1.0.0")


class TaskIn(BaseModel):
    title: str
    done: bool = False


class TaskOut(TaskIn):
    id: str

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskIn, db: Session = Depends(get_db)):
    db_task = Task(id=str(uuid4()), title=task.title, done=task.done)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: str, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: str, task: TaskIn, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.done = task.done
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()