
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(pattern=r"^\d{10}$")
    status: Literal["active", "inactive"] = "active"


class TaskInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: Literal["pending", "in_progress", "done"]


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(pattern=r"^\d{10}$")
    status: Literal["active", "inactive"]
    tasks: list[TaskInfo] = Field(default_factory=list)
