from typing import List
from fastapi import APIRouter, HTTPException, status

from app.models.users import User
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_or_update_clerk_user, get_user_by_clerk_id, get_user_by_id


router = APIRouter()


@router.post('/create', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserCreate):
    """
    Create or sync a user record.
    """
    db_user = await create_or_update_clerk_user(
        clerk_id=user.clerk_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        avatar_url=user.avatar_url,
    )
    return db_user


@router.get('/all', response_model=List[UserResponse])
async def get_users(limit: int = 20, skip: int = 0):
    """
    List registered users.
    """
    users = await User.find_all(limit=limit, skip=skip).to_list()
    return users


@router.get('/by-clerk/{clerk_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_clerk(clerk_id: str):
    """
    Retrieve user record by their Clerk ID.
    """
    user = await get_user_by_clerk_id(clerk_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: str):
    """
    Retrieve user by MongoDB ObjectId.
    """
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user