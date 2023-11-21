from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from database import SessionLocal
import models, schemas
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "00f73470e53d6bbd83ff23e0a14c4e688d4f64ca4ffb2faa14c9180eae33e194"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# To hash password
def get_hashed_password(password):
    return pwd_context.hash(password)

# To verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# To create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# To authenticate user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# To get user from database
def get_user(username: str):
    db = SessionLocal()
    user = db.query(models.UserDb).filter(models.UserDb.username == username).first()
    db.close()
    return user

# To create user
def create_user(db: Session, user_in: schemas.UserCreate):
    hashed_password = get_hashed_password(user_in.password)
    db_user = models.UserDb(id = user_in.id, username=user_in.username, full_name=user_in.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.flush()

    new_user = db.query(models.UserDb).filter(models.UserDb.username == user_in.username).first()
    return new_user

# To update user status
def update_user_status(username: str):
    user = get_user(username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.is_active is False:
        user.is_active = True
        
    return user

# To get the current user which is logged in
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Update user status if inactive
    user = update_user_status(username=token_data.username)
    
    return user

def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# -------------------------------------------------------------------------------------------------------
# Task Functions

#Retrieves all the tasks for the user.
def get_tasks_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):

    # Query to find the User by their ID
    user = db.query(models.UserDb).filter(models.UserDb.id == user_id).first()

    if user:
        # If the user exists, retrieve their tasks
        db_task = db.query(models.TaskDb).filter(models.TaskDb.user_id == user_id).offset(skip).limit(limit).all()
    else:
        raise HTTPException(status_code=404, detail= "User not found")
    return db_task


#Retrieves the task related to a specific ID.
def get_tasks_by_id(db: Session, user_id: int, task_id: int):
    # Query to find the User by their ID
    user = db.query(models.UserDb).filter(models.UserDb.id == user_id).first()

    if not user:
        # If the user doesn't exist, raise an HTTPException or handle accordingly
        raise HTTPException(status_code=404, detail="User not found")

    # Query to find the task by its ID and user ID
    db_task = db.query(models.TaskDb).filter(models.TaskDb.id == task_id, models.TaskDb.user_id == user_id).first()

    if not db_task:
        # If the task doesn't exist for that user, raise an HTTPException or handle accordingly
        raise HTTPException(status_code=404, detail="Task not found")
    
    return db_task

#Creates a new task.
def create_task_for_user(
        payload: schemas.TaskBase, db: Session
        ):

    try:

        #new_note takes the whole dictionary as input and converts the key-value pair to key-value arguments.
        new_task = models.TaskDb(**payload.dict())

        #the below command adds the data to database.
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return {"status": "success", "note": f"The entered task is:\n{new_task}"}
    
    except Exception:

        #Reutrns error when the input format does not match the format of the schema
        #Error 422 is "Unprocessable Entity"
        raise HTTPException(status_code=422, detail=str(Exception))


#Deletes a particular task taking ID as input.
def delete_task_for_user(db: Session, user_id: int, task_id: int):
    # Query to find the User by their ID
    user = db.query(models.UserDb).filter(models.UserDb.id == user_id).first()

    if not user:
        # If the user doesn't exist, raise an HTTPException or handle accordingly
        raise HTTPException(status_code=404, detail="User not found")

    # Query to find the task by its ID and user ID
    db_task = db.query(models.TaskDb).filter(models.TaskDb.id == task_id, models.TaskDb.user_id == user_id).first()

    if not db_task:
        # If the task doesn't exist for that user, raise an HTTPException or handle accordingly
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Deletes the task
    db.delete(db_task)
    db.commit()

    return db_task


#Updates a particular task taking ID as input.
def update_task_for_user(db: Session, user_id: int, task_id: int, task: schemas.TaskBase):
    # Query to find the User by their ID
    user = db.query(models.UserDb).filter(models.UserDb.id == user_id).first()

    if not user:
        # If the user doesn't exist, raise an HTTPException or handle accordingly
        raise HTTPException(status_code=404, detail="User not found")

    # Query to find the task by its ID and user ID
    db_task = db.query(models.TaskDb).filter(models.TaskDb.id == task_id, models.TaskDb.user_id == user_id).first()

    if not db_task:
        # If the task doesn't exist for that user, raise an HTTPException or handle accordingly
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task fields based on input
    for field, value in task.dict(exclude_unset=True).items():
        setattr(db_task, field, value)

    # Commit changes
    db.commit()
    db.refresh(db_task)

    return db_task
