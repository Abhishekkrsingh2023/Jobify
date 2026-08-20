from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from beanie import PydanticObjectId

class UserBase(BaseModel):
    clerk_id: str = Field(..., description="The unique Clerk User ID.", example="user_2abcdef123456")
    email: EmailStr = Field(..., description="The email address of the user.", example="johndoe@example.com")
    first_name: Optional[str] = Field(default=None, description="The first name of the user.", example="John")
    last_name: Optional[str] = Field(default=None, description="The last name of the user.", example="Doe")
    full_name: Optional[str] = Field(default=None, description="The full name of the user.", example="John Doe")
    username: Optional[str] = Field(default=None, description="The unique username of the user.", example="johndoe")
    avatar_url: Optional[str] = Field(default=None, description="Avatar image URL.", example="https://images.clerk.dev/...")
    is_active: bool = Field(default=True, description="Indicates whether the user account is active.")
    is_superuser: bool = Field(default=False, description="Indicates whether the user has superuser privileges.")
    
class UserCreate(UserBase):
    pass
    
class UserResponse(UserBase):
    id: PydanticObjectId = Field(..., description="The unique MongoDB identifier of the user.")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp.")
    updated_at: Optional[datetime] = Field(default=None, description="Last updated timestamp.")
    
    model_config = ConfigDict(from_attributes=True)

class WebhookResponse(BaseModel):
    status: str = Field(..., example="success")
    event: str = Field(..., example="user.created")
    user_id: Optional[str] = Field(default=None, example="user_2abcdef123456")
    message: Optional[str] = Field(default=None)

    