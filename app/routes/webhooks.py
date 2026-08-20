import json
import logging
from typing import Dict, Any
from fastapi import APIRouter, Request, HTTPException, Header, status
from svix.webhooks import Webhook, WebhookVerificationError

from app.configs.settings import settings
from app.crud.user import create_or_update_clerk_user, delete_clerk_user
from app.schemas.user import WebhookResponse

logger = logging.getLogger("jobify.webhooks")
router = APIRouter()


@router.post("/clerk", response_model=WebhookResponse, status_code=status.HTTP_200_OK)
async def clerk_webhook(
    request: Request,
    svix_id: str = Header(None, alias="svix-id"),
    svix_timestamp: str = Header(None, alias="svix-timestamp"),
    svix_signature: str = Header(None, alias="svix-signature"),
):
    """
    Handle incoming webhooks from Clerk.
    Verifies the Svix signature and handles events such as user.created, user.updated, and user.deleted.
    """
    body_bytes = await request.body()

    # Verify signature if secret is configured
    if settings.CLERK_WEBHOOK_SECRET:
        if not svix_id or not svix_timestamp or not svix_signature:
            logger.error("Missing Svix signature headers")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required svix headers",
            )
        try:
            wh = Webhook(settings.CLERK_WEBHOOK_SECRET)
            headers: Dict[str, str] = {
                "svix-id": svix_id,
                "svix-timestamp": svix_timestamp,
                "svix-signature": svix_signature,
            }
            wh.verify(body_bytes, headers)
        except WebhookVerificationError as e:
            logger.error(f"Clerk webhook signature verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid webhook signature",
            )
    else:
        logger.warning(
            "CLERK_WEBHOOK_SECRET is not configured in settings. Parsing webhook payload without verification."
        )

    try:
        event_payload = json.loads(body_bytes.decode("utf-8"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON payload: {e}",
        )

    event_type = event_payload.get("type", "")
    data: Dict[str, Any] = event_payload.get("data", {})
    clerk_user_id = data.get("id")

    logger.info(f"Received Clerk webhook event: {event_type} for user: {clerk_user_id}")

    # Extract user attributes from Clerk payload
    if event_type in ["user.created", "user.create", "user.updated"]:
        email_addresses = data.get("email_addresses", [])
        primary_email_id = data.get("primary_email_address_id")
        
        email = None
        if primary_email_id and email_addresses:
            for item in email_addresses:
                if item.get("id") == primary_email_id:
                    email = item.get("email_address")
                    break
        if not email and email_addresses:
            email = email_addresses[0].get("email_address")
        
        if not email:
            email = f"{clerk_user_id}@clerk.placeholder"

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        avatar_url = data.get("image_url") or data.get("profile_image_url")

        user = await create_or_update_clerk_user(
            clerk_id=clerk_user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            avatar_url=avatar_url,
        )

        return WebhookResponse(
            status="success",
            event=event_type,
            user_id=user.clerk_id,
            message=f"User {user.clerk_id} synchronized successfully.",
        )

    elif event_type in ["user.deleted", "user.delete"]:
        deleted = await delete_clerk_user(clerk_user_id)
        return WebhookResponse(
            status="success" if deleted else "not_found",
            event=event_type,
            user_id=clerk_user_id,
            message=f"User {clerk_user_id} removed from database.",
        )

    return WebhookResponse(
        status="ignored",
        event=event_type,
        user_id=clerk_user_id,
        message=f"Unhandled event type: {event_type}",
    )
