from agents.planner import create_plan
from agents.coder import create_project
from agents.manager import create_manager_plan
from tools.file_tools import write_project_files
from tools.test_tools import check_python_files
from agents.debugger import debug_project
from agents.reviewer import review_project
from agents.architect import design_architecture
from agents.researcher import research_project
from state.state import AgentState


def planner_node(state: AgentState) -> AgentState:
    plan = create_plan(state["user_request"])

    return {
        **state,
        "development_plan": plan,
        "status": "planning_complete",
    }


def coder_node(state: AgentState) -> AgentState:
    print("\n👨‍💻 CODER NODE STARTED")
    plan = state["manager_plan"]
    architecture = state["architecture_plan"]
    test_results=state.get("test_results"),
    review = state.get("review")

    if plan is None:
        raise ValueError("Development plan is missing.")
    
    if architecture is None:
        raise ValueError("Architecture plan is missing.")
    
    print("\n=== ARCHITECTURE RECEIVED BY CODER ===")
    print(architecture.model_dump_json(indent=2))
    print("=== END ARCHITECTURE RECEIVED ===")

    project = create_project(plan,architecture,review)

    generated_files = {
        file.path: file.content
        for file in project.files
    }

    return {
        **state,
        "generated_files": generated_files,
        "status": "coding_complete",
    }


def file_writer_node(state: AgentState) -> AgentState:
    generated_files = state["generated_files"]

    if generated_files is None:
        raise ValueError("Generated files are missing.")

    project_root = write_project_files(generated_files)

    return {
        **state,
        "project_root": project_root,
        "status": "files_written",
    }

def tester_node(state: AgentState) -> AgentState:
    project_root = state["project_root"]

    if project_root is None:
        raise ValueError("Project root is missing.")

    test_results = check_python_files(project_root)

    if test_results.startswith("TEST PASSED"):
        status = "tests_passed"
    else:
        status = "tests_failed"

    return {
        **state,
        "test_results": test_results,
        "status": status,
    }

def debugger_node(state: AgentState) -> AgentState:   
    generated_files = state["generated_files"]
    test_results = state["test_results"]

    if generated_files is None:
        raise ValueError("Generated files are missing.")

    if test_results is None:
        raise ValueError("Test results are missing.")

    project = debug_project(
        generated_files,
        test_results,
    )

    corrected_files = {
        file.path: file.content
        for file in project.files
    }    
    return {
        **state,
        "generated_files": corrected_files,
        "debug_attempts": state["debug_attempts"] + 1,
        "status": "debugging_complete",
    }

def reviewer_node(state: AgentState) -> AgentState:
    user_request = state["user_request"]
    development_plan = state["manager_plan"]
    architecture_plan=state["architecture_plan"]
    generated_files = state["generated_files"]
    test_results = state["test_results"]
    research = state["research"]

    if development_plan is None:
        raise ValueError("Development plan is missing.")

    if generated_files is None:
        raise ValueError("Generated files are missing.")

    if test_results is None:
        raise ValueError("Test results are missing.")

    if architecture_plan is None:
            raise ValueError("Architecture is missing.")

    if research is None:
            raise ValueError("Research results are missing.")

    review = review_project(
        user_request,
        development_plan,
        research,
        architecture_plan,
        generated_files,
        test_results,
    )

    # if state.get("review_attempts", 0) == 0:
    #     review.approved = False
    #     review.issues = [{
    #         "category": "code_style",
    #         "severity": "medium",
    #         "description": "Please add docstrings to all routes in main.py",
    #         "expected": "Docstrings on API endpoints"
    #     }]

    return {
    **state,
    "review": review,
    "review_attempts": state["review_attempts"] + 1,
    "status": "review_approved" if review.approved else "review_rejected",
    }

def architect_node(state: AgentState) -> AgentState:
    plan = state.get("manager_plan")
    research = state["research"]

    if plan is None:
        raise ValueError("Development plan is missing.")

    architecture = design_architecture(plan,research)

    return {
        **state,
        "architecture_plan": architecture,
        "status": "architecture_complete",
    }

def researcher_node(state):
    print("\n🔎 RESEARCHER NODE STARTED")

    research = research_project(
        state["manager_plan"]
    )

    print("\n=== RESEARCH RESULTS ===")
    print(research.model_dump_json(indent=2))
    print("=== END RESEARCH RESULTS ===")

    return {
        "research": research
    }


def manager_node(state: AgentState) -> AgentState:
    print("\n📋 MANAGER NODE STARTED")
    user_request = state.get("user_request", "")
    
    manager_plan = create_manager_plan(user_request)
    
    print("\n=== MANAGER PLAN ===")
    print(manager_plan.model_dump_json(indent=2))
    print("=== END MANAGER PLAN ===\n")
    
    return {
        **state,
        "manager_plan": manager_plan,
        "status": "manager_completed"
    }