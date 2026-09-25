import logging

from fastapi import HTTPException, status
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.settings import settings
from app.schemas.job_schema import JobifyAnalysisRequest

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# LLM + chain — built once at module load, reused across requests
# ---------------------------------------------------------------------------

_llm = ChatGoogleGenerativeAI(
    model=settings.MODEL_NAME,
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0,
)

_SYSTEM = """\
You are an expert technical recruiter. Evaluate the candidate against the \
JOB DESCRIPTION using ONLY the provided RESUME and SELF-DESCRIPTION.

### Grounding
* Never invent skills, experience, projects, qualifications, or facts.
* If inferred, label it as inference in the explanation.
* Missing information → "unknown" where the schema allows it.

### Evaluation Rules
* matched: candidate level ≥ required level with direct evidence.
* partial: skill exists but below required level, or evidence only implied.
* missing: skill required but no evidence found.
* match_percentage: reflect evidence strength and level gap; avoid round scores.
* score_breakdown weights must sum to 1.0.
* readiness: factor in overall_score AND the worst unresolved skill_gap severity.
* skill_gaps: only partial or missing skills.
* strengths: only matched skills with strong evidence.
* Write summary last so it is consistent with scores, strengths, and gaps.\
"""

_HUMAN = """\
RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

SELF-DESCRIPTION:
{self_description}\
"""

_prompt = ChatPromptTemplate.from_messages(
    [("system", _SYSTEM), ("human", _HUMAN)]
)

# with_structured_output uses Gemini's native JSON-schema mode.
# with_retry retries up to 3 times with exponential backoff on any transient
# error (503 / 429 / 500) — no extra code needed.
_chain = _prompt | _llm.with_structured_output(
    JobifyAnalysisRequest,
    method="json_mode",
).with_retry(stop_after_attempt=3, wait_exponential_jitter=True)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


async def generate_job_analysis(
    resume_text: str,
    job_description: str,
    self_description: str,
) -> JobifyAnalysisRequest:
    """
    Analyze a resume against a job description using Gemini via LangChain.

    Retries up to 3× with exponential backoff on transient API errors.

    Args:
        resume_text: Extracted text from the candidate's PDF resume.
        job_description: Raw job description text.
        self_description: Candidate's self-written description.

    Returns:
        JobifyAnalysisRequest: Validated Pydantic model with the full analysis.

    Raises:
        HTTPException 503: If the AI service is unavailable after all retries.
    """
    try:
        result = await _chain.ainvoke(
            {
                "resume_text": resume_text,
                "job_description": job_description,
                "self_description": self_description,
            }
        )
        return result  # type: ignore[return-value]
    except Exception as e:
        logger.exception("Gemini API failed after retries")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable. Please try again shortly.",
        ) from e


if __name__ == "__main__":
    import asyncio

    async def main() -> None:
        result = await generate_job_analysis(
            resume_text="Your resume text here",
            job_description="Your job description here",
            self_description="Your self-description here",
        )
        print(result)

    asyncio.run(main())
