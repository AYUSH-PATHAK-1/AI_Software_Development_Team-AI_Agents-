from typing import List

from pydantic import BaseModel, Field


class DevelopmentPlan(BaseModel):
    requirements: list[str] = Field(
        description="The functional requirements of the software"
    )

    technical_approach: str = Field(
        description="The overall technical approach"
    )

    files_needed: list[str] = Field(
        description="Files that should be created or modified"
    )

    implementation_steps: list[str] = Field(
        description="Ordered implementation steps"
    )

class GeneratedFile(BaseModel):
    path: str = Field(
    description="Relative path of the generated file"
    )

    content: str = Field(
        description="Complete contents of the file"
    )

class GeneratedProject(BaseModel):
    files: list[GeneratedFile] = Field(
    description="Files generated for the project"
    )
class ReviewIssue(BaseModel):
    category: str
    severity: str
    description: str
    expected: str


class ReviewResult(BaseModel):
    approved: bool
    issues: list[ReviewIssue]
    summary: str

class ArchitecturePlan(BaseModel):
    architecture: str
    components: list[str]
    files: list[str]
    data_flow: str
    technical_decisions: list[str]

class ResearchResult(BaseModel):
    findings: list[str]
    recommendations: list[str]
    technologies: list[str]
    risks: list[str]


class TaskBreakdown(BaseModel):
    task_id: int = Field(description="Numerical ID of the sub-task")
    title: str = Field(description="Short summary of the sub-task")
    description: str = Field(description="Detailed explanation of what needs to be implemented")
    assigned_agent: str = Field(description="Target agent for this task (e.g., Researcher, Architect, Coder)")

class ManagerPlan(BaseModel):
    project_name: str = Field(description="Short name for the project")
    summary: str = Field(description="High-level understanding of the user request")
    requirements: List[str] = Field(description="Extracted functional requirements")
    tasks: List[TaskBreakdown] = Field(description="Structured breakdown of tasks for team execution")
    potential_risks: List[str] = Field(description="High-level risks or constraints identified early")
