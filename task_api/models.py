from sqlalchemy import Column, Integer, String, DateTime, Date, Enum

from database import Base

class Task(Base):
    #Specifying the name of the table
    __tablename__ = "tasks"

    #Specifying the columns of the table
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    deadline = Column(Date, index=True, default=None)
    reminder = Column(DateTime, index=True, default=None)
    status = Column(Enum('Pending', 'Completed'), index=True, default='Pending')
    priority = Column(Enum('High', 'Medium', 'Low'), index=True, default='Medium')
