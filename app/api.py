from fastapi import APIRouter, status

from app.routes import users, job_match, webhooks

router = APIRouter()


router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(job_match.router, prefix="/job-match", tags=["Job Match"])
router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])

@router.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "Welcome to Jobify API!"}