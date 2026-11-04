from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED)
def add_user(user_data: UserCreate):
    return create_user(user_data)


@router.get("/users")
def read_users():
    return get_all_users()


@router.get("/users/{user_id}")
def read_user(user_id: int):
    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/users/{user_id}")
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