from google.genai import Client

from app.core.settings import settings
from app.schemas.job_schema import JobifyAnalysisRequest

client = Client(
    api_key=settings.GEMINI_API_KEY
)

async def generate_job_analysis(
    resume_text: str,
    job_description: str, 
    self_description: str,
) -> JobifyAnalysisRequest:
    """
    Analyze a job description using the Gemini API (async).

    Args:
        resume_text (str): The text content of the candidate's resume.
        job_description (str): The job description to analyze.
        self_description (str): The candidate's self-description.

    Returns:
        JobifyAnalysisRequest: The analysis result as a Pydantic model.
    """
    prompt = f"""
You are an expert technical recruiter. Evaluate the candidate against the JOB DESCRIPTION using only the RESUME, JOB DESCRIPTION, and SELF-DESCRIPTION.

### Grounding
* Never invent skills, experience, projects, qualifications, or facts.
* Every `evidence` item must quote/trace to a specific phrase in the RESUME or SELF-DESCRIPTION.
* No evidence → `evidence: []`.
* If inferred, label it as inference in the relevant explanation.
* Missing information → `"unknown"` where allowed, otherwise `"not specified"`.

### Evaluation Rules
* `matched`: candidate level ≥ required level with direct evidence.
* `partial`: skill exists but is below required level, or evidence is only implied.
* `missing`: skill is required but has no evidence.
* `match_percentage`: reflect both evidence strength and level gap; avoid arbitrary round scores.
* `score_breakdown`: `weight` = job importance, `score` = candidate performance; weights must sum to `1.0`.
* `readiness`: consider both `overall_score` and the severity of the worst unresolved `skill_gap`. A critical unresolved gap prevents `almost_ready`/`ready`.
* `skill_gaps` may contain only skills marked `partial` or `missing`.
* `strengths` may contain only `matched` skills with strong evidence.
* Write `summary` last so it is consistent with the scores, strengths, and gaps.

### Input
RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SELF-DESCRIPTION:
{self_description}
"""
    # async call to the Gemini API to analyze the job description
    interaction = await client.aio.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": JobifyAnalysisRequest.model_json_schema(),
        },
    )
    
    return JobifyAnalysisRequest.model_validate_json(interaction.output_text)


if __name__ == "__main__":
    import asyncio

    async def main():
        result = await generate_job_analysis(
            resume_text="Your resume text here",
            job_description="Your job description here",
            self_description="Your self-description here"
        )
        print(result)

    asyncio.run(main())