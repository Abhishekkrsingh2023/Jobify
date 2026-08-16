from app.models import JobAnalysis
from app.services.ai_response import generate_job_analysis


async def analyse_job_details(
    user_id: str,
    resume_text: str,
    job_description: str,
    self_description: str,
) -> JobAnalysis:
    """
    Create a new JobAnalysis document in the database.

    Args:
        user_id (str): The ID of the user who submitted the job analysis.
        resume_text (str): The text content of the candidate's resume.
        job_description (str): The job description to analyze.
        self_description (str): The candidate's self-description.

    Returns:
        JobAnalysis: The created JobAnalysis document.
    """
    analysis = await generate_job_analysis(
        resume_text=resume_text,
        job_description=job_description,
        self_description=self_description
    )

    job_analysis = JobAnalysis(
        user_id=user_id,
        job_info=analysis.job_info,
        candidate_profile=analysis.candidate_profile,
        resume_text=resume_text,
        self_description=self_description,
        jobify_analysis=analysis.jobify_analysis,
    )

    await job_analysis.insert()
    return job_analysis
