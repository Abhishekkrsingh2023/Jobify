from beanie import Document
from pydantic import Field, EmailStr



class User(Document):
    username: str = Field(..., description="The unique username of the user.")
    email: EmailStr = Field(..., description="The email address of the user.")
    full_name: str = Field(..., description="The full name of the user.")
    hashed_password: str = Field(..., description="The hashed password of the user.")
    is_active: bool = Field(default=True, description="Indicates whether the user account is active.")
    is_superuser: bool = Field(default=False, description="Indicates whether the user has superuser privileges.")

    class Settings:
        name = "users"  # Collection name in MongoDB