from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# -------------------------
# Job Information
# -------------------------


class JobInfo(BaseModel):
    title: str = Field(description="The title of the job position.")
    company: str | None = Field(
        description="The name of the company offering the job position.", default=None
    )
    location: str | None = Field(
        description="The location of the job position.", default=None
    )
    employment_type: str | None = Field(
        description="The type of employment, e.g., 'full-time', 'part-time', 'contract'.",
        default=None,
    )
    salary_range: str | None = Field(
        description="The salary range for the job position, if available.", default=None
    )
    experience_required: str | None = Field(
        description="The experience required for the job position, if specified.",
        default=None,
    )
    skills_required: list[str] = Field(
        description="A list of skills required for the job position.",
        default_factory=list,
    )

    model_config = ConfigDict(extra="forbid", from_attributes=True)


# -------------------------
# Candidate Profile
# -------------------------


class CandidateProfile(BaseModel):
    experience_years: float | None = Field(
        description="The number of years of experience the candidate has.", default=None
    )
    tech_stack: list[str] = Field(
        description="A list of technologies the candidate is proficient in.",
        default_factory=list,
    )
    domains: list[str] = Field(
        description="A list of domains the candidate has experience in.",
        default_factory=list,
    )
    education: str | None = Field(
        description="The highest level of education the candidate has achieved.",
        default=None,
    )

    model_config = ConfigDict(extra="forbid", from_attributes=True)


# -------------------------
# Skill Analysis
# -------------------------


class SkillAnalysis(BaseModel):
    skill: str = Field(description="The name of the skill being analyzed.")
    importance: Literal["low", "medium", "high", "critical"] = Field(
        description="The importance of the skill for the job."
    )
    required_level: Literal["beginner", "intermediate", "advanced", "expert"] = Field(
        description="The required proficiency level for the skill."
    )
    candidate_level: Literal[
        "unknown", "beginner", "intermediate", "advanced", "expert"
    ] = Field(description="The candidate's proficiency level in the skill.")
    status: Literal["matched", "partial", "missing", "unknown"] = Field(
        description="The skill match status between the candidate and job requirements."
    )
    match_percentage: float = Field(
        ge=0,
        le=100,
        description="Percentage match between the candidate's skill level and the required level.",
    )


# -------------------------
# Skill Gap
# -------------------------


class SkillGap(BaseModel):
    skill: str = Field(description="The skill with a gap.")
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Severity of the skill gap."
    )
    current_level: str = Field(description="The candidate's current proficiency level.")
    required_level: str = Field(description="The required proficiency level for the job.")
    reason: str = Field(
        description="Why this gap exists and its impact on the candidate's ability to perform."
    )
    recommended_action: str = Field(
        description="What the candidate should do to close this gap."
    )
    estimated_learning_days: int | None = Field(
        ge=0,
        description="Estimated days to reach the required level, if applicable.",
        default=None,
    )


# -------------------------
# Score Breakdown
# -------------------------


class ScoreComponent(BaseModel):
    score: float = Field(
        ge=0, le=100, description="Score for the component, ranging from 0 to 100."
    )
    weight: float = Field(
        ge=0, le=1, description="Weight of this component; all weights must sum to 1.0."
    )


class ScoreBreakdown(BaseModel):
    technical_skills: ScoreComponent
    experience: ScoreComponent
    projects: ScoreComponent
    education: ScoreComponent | None = None


# -------------------------
# Interview Questions
# -------------------------


class InterviewQuestion(BaseModel):
    question: str = Field(description="The interview question text.")
    category: Literal[
        "technical",
        "behavioral",
        "system_design",
        "problem_solving",
        "project",
        "situational",
    ] = Field(description="Category of the interview question.")
    difficulty: Literal["easy", "medium", "hard", "expert"] = Field(
        description="Difficulty level of the interview question."
    )
    skill: str | None = Field(
        description="The skill being assessed, if applicable.",
        default=None,
    )
    answer_guideline: str = Field(
        description="Key points the candidate's answer should cover."
    )
    candidate_specific: bool = Field(
        description="Whether the question is tailored to this specific candidate.",
        default=False,
    )


# -------------------------
# Preparation Roadmap
# -------------------------


class PreparationTask(BaseModel):
    task: str = Field(description="Description of the preparation task.")
    type: Literal["learn", "practice", "build", "revise", "mock_interview"] = Field(
        description="Type of the preparation task."
    )


class PreparationPhase(BaseModel):
    phase: int = Field(ge=1, description="The phase number in the preparation roadmap.")
    title: str = Field(description="Title of the preparation phase.")
    duration_days: int = Field(ge=1, description="Duration of the phase in days.")
    skills: list[str] = Field(description="Skills to focus on during this phase.")
    milestone: str = Field(description="Milestone to achieve by the end of this phase.")
    tasks: list[PreparationTask]


# -------------------------
# Strengths
# -------------------------


class CandidateStrength(BaseModel):
    skill: str = Field(description="The skill in which the candidate excels.")
    reason: str = Field(description="Why the candidate is strong in this skill.")


# -------------------------
# Recommendation
# -------------------------


class Recommendation(BaseModel):
    priority: Literal["low", "medium", "high", "critical"] = Field(
        description="Priority level of the recommendation."
    )
    title: str = Field(description="Title of the recommendation.")
    action: str = Field(description="Concrete action to take.")


# -------------------------
# Final Analysis
# -------------------------


class JobifyAnalysis(BaseModel):
    overall_score: float = Field(
        ge=0,
        le=100,
        description="Overall match score, ranging from 0 to 100.",
    )
    readiness: Literal[
        "not_ready", "needs_preparation", "almost_ready", "job_ready", "strong_match"
    ] = Field(description="Candidate's readiness level for the job.")
    score_breakdown: ScoreBreakdown
    summary: str = Field(
        description="Concise summary of key findings, consistent with the scores and gaps."
    )
    strengths: list[CandidateStrength]
    skills: list[SkillAnalysis]
    skill_gaps: list[SkillGap]
    technical_questions: list[InterviewQuestion]
    behavioral_questions: list[InterviewQuestion]
    preparation_plan: list[PreparationPhase]
    recommendations: list[Recommendation]

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class JobifyAnalysisRequest(BaseModel):
    job_info: JobInfo
    candidate_profile: CandidateProfile
    jobify_analysis: JobifyAnalysis

    model_config = ConfigDict(extra="forbid", from_attributes=True)
