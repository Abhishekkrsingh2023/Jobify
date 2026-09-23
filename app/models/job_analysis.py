from datetime import datetime

from beanie import Document
from pydantic import Field

from app.schemas.job_schema import CandidateProfile, JobifyAnalysis, JobInfo
from app.utils.date_time_utils import get_current_utc_time


class JobAnalysis(Document):
    user_id: str = Field(
        ..., description="The ID of the user who submitted the job analysis."
    )
    job_info: JobInfo
    candidate_profile: CandidateProfile
    jobify_analysis: JobifyAnalysis
    self_description: str | None = Field(
        None, description="The candidate's self-description."
    )
    resume_text: str | None = Field(
        None, description="The text content of the candidate's resume."
    )

    analysis_version: str = Field(
        default="1.0", description="The version of the analysis schema used."
    )

    created_at: datetime = Field(
        default_factory=get_current_utc_time,
        description="The timestamp when the job analysis was created.",
    )
    updated_at: datetime = Field(
        default_factory=get_current_utc_time,
        description="The timestamp when the job analysis was last updated.",
    )

    class Settings:
        name = "job_analysis"
