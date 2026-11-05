
from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)

router = APIRouter()


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def add_user(user_data: UserCreate):
    return create_user(user_data)


@router.get("/users", response_model=list[UserResponse])
def read_users():
    return get_all_users()


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def edit_user(user_id: int, user_data: UserCreate):
    user = update_user(user_id, user_data)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/users/{user_id}")
def remove_user(user_id: int):
    deleted = delete_user(user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}
