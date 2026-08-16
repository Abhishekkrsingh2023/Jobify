from pydantic import BaseModel, Field, EmailStr, ConfigDict
from beanie import PydanticObjectId

class UserBase(BaseModel):
    username: str = Field(..., description="The unique username of the user.", example="johndoe")
    email: EmailStr = Field(..., description="The email address of the user.", example="johndoe@example.com")
    full_name: str = Field(..., description="The full name of the user.", example="John Doe")
    is_active: bool = Field(default=True, description="Indicates whether the user account is active.")
    is_superuser: bool = Field(default=False, description="Indicates whether the user has superuser privileges.")
    
class UserCreate(UserBase):
    password: str = Field(..., description="The password of the user.", example="securepassword123")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "full_name": "John Doe",
                "password": "securepassword123",
                "is_active": True,
                "is_superuser": False
            }
        }
    )
    
class UserResponse(UserBase):
    id: PydanticObjectId = Field(..., description="The unique identifier of the user.")
    
    model_config = ConfigDict(from_attributes=True)
    