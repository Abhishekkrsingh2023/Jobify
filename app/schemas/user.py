from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    clerk_id: str = Field(
        ..., description="The unique Clerk User ID.", examples=["user_2abcdef123456"]
    )
    email: EmailStr = Field(
        ...,
        description="The email address of the user.",
        examples=["johndoe@example.com"],
    )
    first_name: str | None = Field(
        default=None, description="The first name of the user.", examples=["John"]
    )
    last_name: str | None = Field(
        default=None, description="The last name of the user.", examples=["Doe"]
    )
    full_name: str | None = Field(
        default=None, description="The full name of the user.", examples=["John Doe"]
    )
    username: str | None = Field(
        default=None,
        description="The unique username of the user.",
        examples=["johndoe"],
    )
    avatar_url: str | None = Field(
        default=None,
        description="Avatar image URL.",
        examples=["https://images.clerk.dev/..."],
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the user account is active."
    )
    is_superuser: bool = Field(
        default=False,
        description="Indicates whether the user has superuser privileges.",
    )


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: PydanticObjectId = Field(
        ..., description="The unique MongoDB identifier of the user."
    )
    created_at: datetime | None = Field(default=None, description="Creation timestamp.")
    updated_at: datetime | None = Field(
        default=None, description="Last updated timestamp."
    )

    model_config = ConfigDict(from_attributes=True)


class WebhookResponse(BaseModel):
    status: str = Field(..., examples=["success"])
    event: str = Field(..., examples=["user.created"])
    user_id: str | None = Field(default=None, examples=["user_2abcdef123456"])
    message: str | None = Field(default=None)
