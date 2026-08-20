import httpx
from fastapi import Request, HTTPException, status
from clerk_backend_api import Clerk
from clerk_backend_api.security import AuthenticateRequestOptions

from app.core.settings import settings

clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)


def _convert_to_httpx_request(fastapi_request: Request) -> httpx.Request:
    return httpx.Request(
        method=fastapi_request.method,
        url=str(fastapi_request.url),
        headers=dict(fastapi_request.headers)
    )


async def get_current_user(request: Request):
    httpx_request = _convert_to_httpx_request(request)

    authorized_parties = list(filter(None, {
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
    }))

    request_state = clerk.authenticate_request(
        httpx_request,
        AuthenticateRequestOptions(authorized_parties=authorized_parties)
    )

    if not request_state.is_signed_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    claims = request_state.payload or {}
    user_id = claims.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    return user_id