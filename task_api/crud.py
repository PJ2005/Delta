from sqlalchemy.orm import Session
from fastapi import HTTPException

import models
import schemas


#Retrieves all the tasks for the user.
def get_tasks_for_user(
        db: Session, skip: int = 0, limit: int = 100
        ):

    #db_task parses through the whole databse and returns all the rows present.
    db_task = db.query(models.Task).offset(skip).limit(limit).all()

    return db_task


#Retrieves the task related to a specific ID.
def get_tasks_by_id(
        db: Session, task_id: int
        ):

    #db_task compares and returns the task matching the ID input by user.
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:

        #Returns the error when no such task with the particular ID exists.
        raise HTTPException(status_code=404, detail="Task not found")
    
    return db_task


#Creates a new task.
def create_task_for_user(
        payload: schemas.TaskBase, db: Session
        ):

    try:

        #new_note takes the whole dictionary as input and converts the key-value pair to key-value arguments.
        new_task = models.Task(**payload.dict())

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
def delete_task_for_user(
        db: Session, task_id: int
        ):

    #Comapres to find the task ID
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:

        #Returns error when no such task with a particular ID exists.
        raise HTTPException(status_code=404, detail="Task not found")
    
    #Deletes the task.
    db.delete(db_task)
    db.commit()

    return db_task


#Updates a particular task taking ID as input.
def update_task_for_user(
        db: Session, task_id: int, task: schemas.TaskBase
        ):

    try:

        #db_task compares and returns the task matching the ID input by user.
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

        if not db_task:

            #Returns error when no such task with a particular ID exists.
            raise HTTPException(status_code=404, detail="Task not found")
        
        #Updates all the fields of the particualr ID.
        db_task.name = task.name
        db_task.description = task.description
        db_task.deadline = task.deadline
        db_task.reminder = task.reminder
        db_task.status = task.status
        db_task.priority = task.priority

        #Commits the changes.
        db.commit()
        db.refresh(db_task)

        return db_task
    
    except Exception:

        #Returns error when the input format does not match the schema format.
        raise HTTPException(status_code=422, detail=str(Exception))