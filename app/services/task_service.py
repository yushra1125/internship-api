from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate


def create_task(db: Session, task_data: TaskCreate):
    user = db.query(User).filter(User.id == task_data.user_id).first()

    if user is None:
        return None

    task = Task(**task_data.model_dump())

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_all_tasks(db: Session, status: str | None = None):
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    return query.all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_data: TaskCreate):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    user = db.query(User).filter(User.id == task_data.user_id).first()

    if user is None:
        return None

    for key, value in task_data.model_dump().items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)

    if task is None:
        return False

    db.delete(task)
    db.commit()

    return True