
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskStudentUpdate


def create_task(db: Session, task_data: TaskCreate):
    user = db.query(User).filter(
        User.id == task_data.user_id,
        User.role == "student",
        User.status == "active"
    ).first()

    if user is None:
        return None

    task = Task(**task_data.model_dump())

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_all_tasks(
    db: Session,
    status: str | None = None,
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    user_id: int | None = None
):
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    if user_id:
        query = query.filter(Task.user_id == user_id)

    offset = (page - 1) * limit

    return query.order_by(Task.id).offset(offset).limit(limit).all()


def get_student_tasks(db: Session, student_id: int):
    return db.query(Task).filter(
        Task.user_id == student_id
    ).all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(
        Task.id == task_id
    ).first()


def update_task(db: Session, task_id: int, task_data: TaskCreate):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    user = db.query(User).filter(
        User.id == task_data.user_id,
        User.role == "student",
        User.status == "active"
    ).first()

    if user is None:
        return None

    for key, value in task_data.model_dump().items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


def update_student_task(
    db: Session,
    task_id: int,
    student_id: int,
    task_data: TaskStudentUpdate
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == student_id
    ).first()

    if task is None:
        return None

    updates = task_data.model_dump(exclude_unset=True)

    for key, value in updates.items():
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
