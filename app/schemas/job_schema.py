from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

# -------------------------
# Job Information
# -------------------------

class JobInfo(BaseModel):
    title: str = Field(description="The title of the job position.")
    company: Optional[str] = Field(description="The name of the company offering the job position.", default=None)
    location: Optional[str] = Field(description="The location of the job position.", default=None)
    employment_type: Optional[str] = Field(description="The type of employment for the job position, e.g., 'full-time', 'part-time', 'contract', etc.", default=None)
    salary_range: Optional[str] = Field(description="The salary range for the job position, if available.", default=None)
    experience_required: Optional[str] = Field(description="The experience required for the job position, if specified.", default=None)
    skills_required: list[str] = Field(description="A list of skills required for the job position.", default_factory=list)
    responsibilities: list[str] = Field(description="A list of responsibilities associated with the job position.", default_factory=list)
    qualifications: list[str] = Field(description="A list of qualifications required for the job position.", default_factory=list)
    description: str = Field(description="A detailed description of the job position.")

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

# -------------------------
# Candidate Profile
# -------------------------

class CandidateProfile(BaseModel):
    experience_years: Optional[float] = Field(description="The number of years of experience the candidate has.", default=None)
    tech_stack: list[str] = Field(description="A list of technologies the candidate is proficient in.", default_factory=list)
    domains: list[str] = Field(description="A list of domains the candidate has experience in.", default_factory=list)
    education: Optional[str] = Field(description="The highest level of education the candidate has achieved.", default=None)
    certifications: list[str] = Field(description="A list of certifications the candidate holds.", default_factory=list)
    projects: list[str] = Field(description="A list of projects the candidate has worked on.", default_factory=list)

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

# -------------------------
# Skill Analysis
# -------------------------

class SkillAnalysis(BaseModel):
    skill: str = Field(description="The name of the skill being analyzed.")
    category: Literal[
        "language",
        "framework",
        "database",
        "devops",
        "cloud",
        "tool",
        "soft_skill",
        "concept",
        "other"
    ] = Field(description="The category of the skill, e.g., 'language', 'framework', 'database', etc.")
    importance: Literal["low", "medium", "high", "critical"] = Field(description="The importance of the skill, e.g., 'low', 'medium', 'high', 'critical'.")
    required_level: Literal[
        "beginner",
        "intermediate",
        "advanced",
        "expert"
    ] = Field(description="The required proficiency level for the skill as per the job requirements.")
    candidate_level: Literal[
        "unknown",
        "beginner",
        "intermediate",
        "advanced",
        "expert"
    ] = Field(description="The candidate's proficiency level in the skill.")
    status: Literal[
        "matched",
        "partial",
        "missing",
        "unknown"
    ] = Field(description="The status of the skill match between the candidate and the job requirements.")
    match_percentage: float = Field(ge=0, le=100, description="The percentage match between the candidate's skill level and the required level for the job.")
    evidence: list[str] = Field(description="Evidence supporting the candidate's skill level, such as projects, certifications, or work experience.", default_factory=list)
    gap_description: Optional[str] = Field(description="Description of the gap between the candidate's skill level and the required level, if applicable.", default=None)


# -------------------------
# Skill Gap
# -------------------------

class SkillGap(BaseModel):
    skill: str = Field(description="The skill that has a gap between the candidate's current level and the required level.")
    category: str = Field(description="The category of the skill, e.g., 'language', 'framework', 'database', etc.")
    severity: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ] = Field(description="Severity of the skill gap, indicating how critical it is for the candidate to address this gap.")
    current_level: str = Field(description="The candidate's current proficiency level in the skill.")
    required_level: str = Field(description="The required proficiency level for the skill as per the job requirements.")
    reason: str = Field(description="Reason explaining why this skill gap exists, providing context for the candidate.")
    impact: str = Field(description="Impact of the skill gap on the candidate's ability to perform in the job role, explaining potential consequences.")
    recommended_action: str = Field(description="Recommended action for the candidate to address the skill gap, providing guidance on how to improve.")
    estimated_learning_days: Optional[int] = Field(ge=0, description="Estimated number of days required for the candidate to learn and improve the skill to the required level, if applicable.", default=None)


# -------------------------
# Score Breakdown
# -------------------------

class ScoreComponent(BaseModel):
    score: float = Field(ge=0, le=100, description="Score for the component, ranging from 0 to 100.")
    weight: float = Field(ge=0, le=1, description="Weight of the component, ranging from 0 to 1.")
    explanation: str = Field(description="Explanation of the score and weight.")


class ScoreBreakdown(BaseModel):
    technical_skills: ScoreComponent
    experience: ScoreComponent
    responsibilities: ScoreComponent
    projects: ScoreComponent
    education: Optional[ScoreComponent] = None


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
        "situational"
    ] = Field(description="Category of the interview question.")
    difficulty: Literal[
        "easy",
        "medium",
        "hard",
        "expert"
    ] = Field(description="Difficulty level of the interview question.")
    skill: Optional[str] = Field(description="The skill associated with the interview question, if applicable.", default=None)
    intention: str = Field(description="The intention behind the interview question, explaining what the interviewer is trying to assess.")
    expected_topics: list[str] = Field(description="List of expected topics or areas that the candidate should cover in their answer.", default_factory=list)
    answer_guideline: str = Field(description="Guidelines for the candidate's answer to the interview question.")
    candidate_specific: bool = Field(description="Indicates if the question is specific to the candidate.", default=False)


# -------------------------
# Preparation Roadmap
# -------------------------

class PreparationTask(BaseModel):
    task: str = Field(description="Description of the preparation task.")
    type: Literal[
        "learn",
        "practice",
        "build",
        "revise",
        "mock_interview"
    ] = Field(description="Type of the preparation task.")
    estimated_hours: Optional[float] = Field(ge=0, description="Estimated hours required to complete the task.", default=None)
    resource_type: Optional[str] = Field(description="Type of resource for the task, e.g., 'video', 'article', 'course', etc.", default=None)


class PreparationPhase(BaseModel):
    phase: int = Field(ge=1, description="The phase number in the preparation roadmap.")
    title: str = Field(description="Title of the preparation phase.")
    objective: str = Field(description="Objective of the preparation phase.")
    duration_days: int = Field(ge=1, description="Duration of the phase in days.")
    skills: list[str] = Field(description="List of skills to be focused on during this phase.")
    milestone: str = Field(description="Milestone to be achieved by the end of this phase.")
    tasks: list[PreparationTask]


# -------------------------
# Strengths
# -------------------------

class CandidateStrength(BaseModel):
    skill: str = Field(description="The skill in which the candidate excels.")
    reason: str = Field(description="The reason why the candidate is strong in this skill.")
    evidence: list[str] = Field(description="Evidence supporting the candidate's strength in this skill.", default_factory=list)


# -------------------------
# Recommendation
# -------------------------

class Recommendation(BaseModel):
    priority: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ] = Field(description="Priority level of the recommendation.")

    title: str = Field(description="Title of the recommendation.")
    description: str = Field(description="Detailed description of the recommendation.")
    action: str = Field(description="Action to be taken for the recommendation.")


# -------------------------
# Final Analysis
# -------------------------

class JobifyAnalysis(BaseModel):
    overall_score: float = Field(ge=0, le=100, description="Overall score of the analysis, ranging from 0 to 100.")

    readiness: Literal[
        "not_ready",
        "needs_preparation",
        "almost_ready",
        "job_ready",
        "strong_match"
    ] = Field(description="Readiness level of the candidate for the job position.")
    confidence_score: float = Field(
        ge=0,
        le=1,
        description="Confidence score of the analysis, ranging from 0 to 1."
    )
    score_breakdown: ScoreBreakdown
    summary: str = Field(description="Summary of the analysis, highlighting key findings and insights.")
    strengths: list[CandidateStrength]
    skills: list[SkillAnalysis]
    skill_gaps: list[SkillGap]
    technical_questions: list[InterviewQuestion]
    behavioral_questions: list[InterviewQuestion]
    preparation_plan: list[PreparationPhase]
    recommendations: list[Recommendation]
    
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )
    
    
class JobifyAnalysisRequest(BaseModel):
    job_info: JobInfo
    candidate_profile: CandidateProfile
    jobify_analysis: JobifyAnalysis
    
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )