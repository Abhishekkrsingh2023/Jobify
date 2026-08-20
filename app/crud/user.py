from typing import Optional
from beanie import PydanticObjectId
from app.models.users import User
from app.utils.date_time_utils import get_current_utc_time


async def create_or_update_clerk_user(
    clerk_id: str,
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    username: Optional[str] = None,
    avatar_url: Optional[str] = None,
) -> User:
    """
    Create a new user or update an existing one based on Clerk webhook data.
    """
    # Try finding existing user by clerk_id or email
    user = await User.find_one({"clerk_id": clerk_id})
    if not user:
        user = await User.find_one({"email": email})

    full_name_parts = [p for p in [first_name, last_name] if p]
    computed_full_name = " ".join(full_name_parts).strip() if full_name_parts else (username or email.split("@")[0])

    if user:
        user.clerk_id = clerk_id
        user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if computed_full_name:
            user.full_name = computed_full_name
        if username is not None:
            user.username = username
        if avatar_url is not None:
            user.avatar_url = avatar_url
        user.updated_at = get_current_utc_time()
        await user.save()
        return user

    new_user = User(
        clerk_id=clerk_id,
        email=email,
        first_name=first_name,
        last_name=last_name,
        full_name=computed_full_name,
        username=username or email.split("@")[0],
        avatar_url=avatar_url,
        is_active=True,
        is_superuser=False,
        created_at=get_current_utc_time(),
        updated_at=get_current_utc_time(),
    )
    await new_user.insert()
    return new_user


async def get_user_by_clerk_id(clerk_id: str) -> Optional[User]:
    """
    Retrieve a user by their unique Clerk ID.
    """
    return await User.find_one({"clerk_id": clerk_id})


async def get_user_by_id(user_id: str) -> Optional[User]:
    """
    Retrieve a user by their MongoDB ObjectId.
    """
    try:
        obj_id = PydanticObjectId(user_id)
        return await User.get(obj_id)
    except Exception:
        return None


async def get_user_by_email(email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.
    """
    return await User.find_one({"email": email})


async def delete_clerk_user(clerk_id: str) -> bool:
    """
    Delete or deactivate a user when deleted in Clerk.
    """
    user = await User.find_one({"clerk_id": clerk_id})
    if user:
        await user.delete()
        return True
    return False