from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from models import Base
import schemas
import crud
from database import SessionLocal, engine

from datetime import timedelta
from sqlalchemy.orm import Session


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

# User Login Token

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/create-user")
def create_user_new(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db=db, user_in=user_in)
    return user

# Task endpoints
# -------------------------------------------------------------------------------------------------------------------


#First endpoint to create and add a task

#task specifes the schema to be used and db uses the database session initialized in the start
@app.post("/add-task/")
#  response_model=schemas.TaskBase
def create_task(task: schemas.TaskBase, current_user: schemas.User = Depends(crud.get_current_active_user), db: Session = Depends(get_db)):
    # `get_current_active_user` is a function that verifies and returns the current user

    # Check if current_user exists (authentication)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    
    task.user_id = current_user.id # newly added
    # Create the task for the authenticated user
    db_task = crud.create_task_for_user(db=db, payload=task)

    if db_task is None:
        # Returns Error if the TaskID exists
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Task ID exists")
    
    return db_task


#second endpoint to retrieve all the tasksZ
@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(crud.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if current_user exists (authentication)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    # Fetch tasks for the authenticated user
    tasks = crud.get_tasks_for_user(db, skip=skip, limit=limit, user_id=current_user.id)

    return tasks


#Third endpoint is to get a task by a specific ID.
@app.get("/tasks/{id}/", response_model=schemas.Task)
def read_tasks_by_id(
    id: int,
    current_user: schemas.User = Depends(crud.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if current_user exists (authentication)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    # Fetch task by ID for the authenticated user
    task = crud.get_tasks_by_id(db, user_id=current_user.id, task_id=id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


#Fourth endpoint is to update a particular task compared through ID.
@app.put("/update-task/{id}/", response_model=schemas.TaskBase)
def update_task(
    id: int,
    task: schemas.TaskBase,
    current_user: schemas.User = Depends(crud.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if current_user exists (authentication)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    db_task = crud.update_task_for_user(db=db, user_id=current_user.id, task=task, task_id=id)

    if db_task is None:
        # Error is raised when the task ID is not found in the database or doesn't belong to the user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return db_task

@app.delete("/delete-task/{id}/", response_model=schemas.Task)
def delete_task(
    id: int,
    current_user: schemas.User = Depends(crud.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if current_user exists (authentication)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    db_task = crud.delete_task_for_user(db=db, user_id=current_user.id, task_id=id)

    if db_task is None:
        # Error is raised when the task ID is not found in the database or doesn't belong to the user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return db_task