from typing import Literal
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(pattern=r"^\d{10}$")
    status: Literal["active", "inactive"] = "active"


class UserResponse(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(pattern=r"^\d{10}$")
    status: Literal["active", "inactive"]