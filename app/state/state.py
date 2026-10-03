from pathlib import Path
from typing import Optional, TypedDict

from agents.schemas import DevelopmentPlan, ManagerPlan, ReviewResult, ArchitecturePlan, ResearchResult


class AgentState(TypedDict):
    user_request: str

    manager_plan: Optional[ManagerPlan]

    development_plan: DevelopmentPlan | None

    research: ResearchResult | None

    architecture_plan: ArchitecturePlan | None

    generated_files: dict[str, str] | None

    project_root: Path | None

    test_results: str | None

    review: ReviewResult | None

    errors: list[str]

    debug_attempts: int

    review_attempts: int

    status: str