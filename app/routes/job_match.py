import io
from fastapi import (
    APIRouter, UploadFile, File, Form, status,
    HTTPException, status, Depends
)

from app.services.pdf_extractor import extract_text_from_pdf
from app.crud.job_matcher import analyse_job_details
from app.core.auth import get_current_user

router = APIRouter()

MAX_FILE_SIZE = 2 * 1024 * 1024
def _validate_resume(resume: UploadFile):
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed.")
    if resume.size and resume.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size exceeds the 2 MB limit.")


@router.post("/analyze", status_code=status.HTTP_201_CREATED)
async def upload_file(
    user_id: str = Depends(get_current_user),
    resume: UploadFile = File(..., description="The resume file to be uploaded."),
    self_description: str = Form(..., description="A brief self-description of the candidate."),
    job_description: str = Form(..., description="The job description for the position being applied for.")
):
    _validate_resume(resume)
    try:
        content = await resume.read()
        resume_text = extract_text_from_pdf(stream=io.BytesIO(content))

        return await analyse_job_details(
            user_id=user_id,
            resume_text=resume_text,
            job_description=job_description,
            self_description=self_description,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to process resume: {e}")