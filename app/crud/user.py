from app.models import User
# class UserBase(BaseModel):
#     email: str = Field(..., description="The unique username of the user.", example="johndoe")
#     full_name: str = Field(..., description="The full name of the user.", example="John Doe")
#     is_active: bool = Field(default=True, description="Indicates whether the user account is active.")
#     is_superuser: bool = Field(default=False, description="Indicates whether the user has superuser privileges.")

async def create_user(email: str, full_name: str) -> User:
    # Logic to create a new user in the database
    new_user = User(email=email, full_name=full_name)
    await new_user.insert()
    return new_user