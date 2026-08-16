from fastapi import APIRouter, HTTPException, status

from app.models import User
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user


router = APIRouter()

@router.post('/create', response_model=UserResponse)
async def create_user(user: UserCreate):
    pass

@router.get('/users', response_model=list[UserResponse])
async def get_users(limit: int = 10, skip: int = 0):
    users = await User.find_all(limit=limit, skip=skip).to_list()
    return users

@router.get('/users/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: str):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user