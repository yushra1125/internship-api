
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TaskStatus = Literal["pending", "in_progress", "done"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str | None = None
    status: TaskStatus = "pending"
    user_id: int


class TaskStudentUpdate(BaseModel):
    status: TaskStatus | None = None
    work_note: str | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    work_note: str | None = None
    user_id: int
