from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

#Task Database Schema
class TaskBase(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    deadline: date
    reminder: Optional[datetime] = None
    status: Optional[str] = 'Pending' #pending is default value to be assigned 
    priority: Optional[str] = 'Medium'#medium is default value to be assigned

    class Config:
        orm_mode = True

class TaskDb(TaskBase):
    id: int

#Helps to parse the incoming JSON request body
    class Config:
        orm_mode = True