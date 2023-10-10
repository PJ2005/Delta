from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from models import Base
from schemas import Task, TaskBase
from crud import create_task, delete_task_for_user, get_tasks, update_task_for_user, get_tasks_by_id
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add-task/response_model=TaskBase")
def create_task_for_user(
    task: TaskBase, db: Session = Depends(get_db)
):
    db_task = create_task(db=db, payload=task)
    return db_task

@app.get("/tasks/", response_model=list[Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{id}", response_model = Task)
def read_tasks_by_id(id: int, db: Session = Depends(get_db)):
    tasks = get_tasks_by_id(db, task_id=id)
    return tasks

@app.put("/update-task/{id}", response_model=TaskBase)
def update_task(
    id: int, task: TaskBase, db: Session = Depends(get_db)
):
    db_task = update_task_for_user(db=db, task=task, task_id=id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/delete-task/{id}", response_model=Task)
def delete_task(
   id: int, db: Session = Depends(get_db)
):
    db_task = delete_task_for_user(db=db, task_id=id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
