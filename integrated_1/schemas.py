from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

#Specifying token schema
class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    username: str
    full_name: str | None = None
    is_active: bool | None = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    id: Optional[int] = None
    username: str
    full_name: str | None = None
    password: str

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


#Task Database Schema
class TaskBase(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    deadline: date
    reminder: Optional[datetime] = None
    status: Optional[str] = 'Pending' #pending is default value to be assigned 
    priority: Optional[str] = 'Medium'#medium is default value to be assigned
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int

#Helps to parse the incoming JSON request body
    class Config:
        orm_mode = True