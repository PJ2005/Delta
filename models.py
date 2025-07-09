from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

# User Database
class UserDb(Base):
    #Specifying the name of the table
    __tablename__ = "users"

    # Specifying the columns of the table
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)

    # Establishing a one-to-many relationship with TaskDb
    tasks = relationship("TaskDb", back_populates="user")

# Task Database
class TaskDb(Base):
    # Specifying the name of the table
    __tablename__ = "tasks"

    # Specifying the columns of the table
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    deadline = Column(Date, index=True, default=None)
    reminder = Column(DateTime, index=True, default=None)
    status = Column(Enum('Pending', 'Completed'), index=True, default='Pending')
    priority = Column(Enum('High', 'Medium', 'Low'), index=True, default='Medium')

    # Establishing a many-to-one relationship with UserDb
    user_id = Column(Integer, ForeignKey(UserDb.id))
    user = relationship("UserDb", back_populates="tasks")
