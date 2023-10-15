from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from models import Base
import schemas
import crud
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

#Intializing an instance of FastAPI
app = FastAPI()

#Intializing database session
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


#First endpoint to create and add a task
@app.post("/add-task/response_model=TaskBase")

#task specifes the schema to be used and db uses the database session initialized in the start
def create_task(task: schemas.TaskBase, db: Session = Depends(get_db)):

    #calls the creating task fucntion
    db_task = crud.create_task_for_user(db=db, payload=task)

    if db_task is None:
        #Returns Error if the TaskID exists
        raise HTTPException(status_code=500, detail="Task ID exists")
    
    return db_task


#second endpoint to retrieve all the tasks
@app.get("/tasks/response_model=list[schemas.TaskDb]")

#The maximum limit of tasks to be displayed at a time is specified in the limit parameter
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    tasks = crud.get_tasks_for_user(db, skip=skip, limit=limit)

    return tasks


#Third endpoint is to get a task by a specific ID.
@app.get("/tasks/{id}/response_model = schemas.TaskDb")

#id contains the ID input by user
def read_tasks_by_id(id: int, db: Session = Depends(get_db)):

    tasks = crud.get_tasks_by_id(db, task_id=id)

    return tasks


#Fourth endpoint is to update a particular task compared through ID.
@app.put("/update-task/{id}/response_model=schemas.TaskBase")

def update_task(
    id: int, task: schemas.TaskBase, db: Session = Depends(get_db)
):
    
    db_task = crud.update_task_for_user(db=db, task=task, task_id=id)

    if db_task is None:
        #Error is raised when the task ID is not found in the database
        raise HTTPException(status_code=404, detail="Task not found")
    
    return db_task


#Fifth endpoint to delete a particular task.
@app.delete("/delete-task/{id}/response_model=schemas.TaskDb")

def delete_task(
   id: int, db: Session = Depends(get_db)
):
    
    db_task = crud.delete_task_for_user(db=db, task_id=id)

    if db_task is None:
        #Error is raised when the task ID is not found in the database
        raise HTTPException(status_code=404, detail="Task not found")
    
    return db_task