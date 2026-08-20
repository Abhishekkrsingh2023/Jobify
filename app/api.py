from fastapi import APIRouter

from app.routes import job_match

router = APIRouter()


router.include_router(job_match.router, prefix="/job-match", tags=["Job Match"])
