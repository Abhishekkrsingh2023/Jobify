from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field, EmailStr
from app.utils.date_time_utils import get_current_utc_time


class User(Document):
    clerk_id: str = Field(..., unique=True, index=True, description="The unique Clerk User ID.")
    email: EmailStr = Field(..., index=True, description="The email address of the user.")
    first_name: Optional[str] = Field(default=None, description="The first name of the user.")
    last_name: Optional[str] = Field(default=None, description="The last name of the user.")
    full_name: Optional[str] = Field(default=None, description="The full name of the user.")
    username: Optional[str] = Field(default=None, description="The unique username of the user.")
    avatar_url: Optional[str] = Field(default=None, description="The avatar/profile image URL.")
    hashed_password: Optional[str] = Field(default=None, description="Optional hashed password.")
    is_active: bool = Field(default=True, description="Indicates whether the user account is active.")
    is_superuser: bool = Field(default=False, description="Indicates whether the user has superuser privileges.")
    created_at: datetime = Field(
        default_factory=get_current_utc_time,
        description="The timestamp when the user was created."
    )
    updated_at: datetime = Field(
        default_factory=get_current_utc_time,
        description="The timestamp when the user was last updated."
    )

    class Settings:
        name = "users"  # Collection name in MongoDB