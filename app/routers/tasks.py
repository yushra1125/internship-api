
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskStudentUpdate
from app.services.task_services import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    get_student_tasks,
    update_task,
    update_student_task,
    delete_task
)
from app.dependencies import (
    get_current_teacher,
    get_current_student
)

router = APIRouter()


# Teacher: Create and assign task
@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
def add_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    task = create_task(db, task_data)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return task


# Teacher: View all tasks with pagination, search and filters
@router.get("/tasks", response_model=list[TaskResponse])
def read_tasks(
    task_status: Literal["pending", "in_progress", "done"] | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None, min_length=1),
    user_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    return get_all_tasks(
        db=db,
        status=task_status,
        page=page,
        limit=limit,
        search=search,
        user_id=user_id
    )


# Student: View own tasks
@router.get("/tasks/my", response_model=list[TaskResponse])
def read_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    return get_student_tasks(db, current_user.id)


# Teacher: View any task
@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# Teacher: Update or reassign task
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def edit_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    task = update_task(db, task_id, task_data)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task or assigned student not found"
        )

    return task


# Student: Update own status and work note
@router.patch(
    "/tasks/{task_id}/work",
    response_model=TaskResponse
)
def edit_my_task(
    task_id: int,
    task_data: TaskStudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    task = update_student_task(
        db, task_id, current_user.id, task_data
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# Teacher: Delete task
@router.delete("/tasks/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher)
):
    deleted = delete_task(db, task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}
