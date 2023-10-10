from sqlalchemy.orm import Session

import models
import schemas

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_tasks_by_id(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    return db_task

def create_task(payload: schemas.TaskBase, db: Session):
    new_note = models.Task(**payload.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"status": "success", "note": new_note}

def delete_task_for_user(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return None
    db.delete(db_task)
    db.commit()
    return db_task

def update_task_for_user(db: Session, task_id: int, task: schemas.TaskBase):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return None
    db_task.name = task.name
    db_task.description = task.description
    db_task.deadline = task.deadline
    db_task.reminder = task.reminder
    db_task.status = task.status
    db_task.priority = task.priority
    db.commit()
    db.refresh(db_task)
    return db_task