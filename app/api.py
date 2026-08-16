from fastapi import APIRouter

from app.routes import users, job_match

router = APIRouter()


router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(job_match.router, prefix="/job-match", tags=["Job Match"])

