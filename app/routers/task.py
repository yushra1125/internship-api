from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task
)

router = APIRouter()


@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
def add_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    task = create_task(db, task_data)

    if task is None:
        raise HTTPException(status_code=404, detail="User not found")

    return task


@router.get("/tasks", response_model=list[TaskResponse])
def read_tasks(
    task_status: Literal["pending", "in_progress", "completed"] | None = None,
    db: Session = Depends(get_db)
):
    return get_all_tasks(db, task_status)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def edit_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    task = update_task(db, task_id, task_data)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task or assigned user not found"
        )

    return task


@router.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    deleted = delete_task(db, task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}