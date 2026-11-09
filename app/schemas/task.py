from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str | None = None
    status: Literal["pending", "in_progress", "completed"] = "pending"
    user_id: int


class TaskStudentUpdate(BaseModel):
    status: Literal["pending", "in_progress", "completed"] | None = None
    work_note: str | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: Literal["pending", "in_progress", "completed"]
    work_note: str | None = None
    user_id: int