# from langchain_ollama import ChatOllama


# llm = ChatOllama(
#     model="gemma4:31b-cloud",
#     temperature=0,
# )


# response = llm.invoke(
#     "Explain what a Python function is in one sentence."
# )

# print(response.content)
from dotenv import load_dotenv

load_dotenv()

from graph.workflow import graph

request = """
Build a FastAPI backend for a simple task management application.
Users should be able to create, read, update, and delete tasks.
"""

initial_state = {
    "user_request": request,
    "development_plan": None,
    "manager_plan": None,
    "generated_files": None,
    "project_root": None,
    "test_results": None,
    "review": None,
    "errors": [],
    "debug_attempts": 0,
    "review_attempts": 0,
    "status": "planning",
}

result = graph.invoke(initial_state)

manager_plan = result.get("manager_plan")

if manager_plan:
    print("\n=== PROJECT SUMMARY ===")
    print(manager_plan.summary)

    print("\n=== FINAL REQUIREMENTS ===")
    for req in manager_plan.requirements:
        print(f"- {req}")

    print("\n=== TASK BREAKDOWN ===")
    for task in manager_plan.tasks:
        print(f"[{task.assigned_agent}] Task {task.task_id}: {task.title}")

    print("\n=== IDENTIFIED RISKS ===")
    for risk in manager_plan.potential_risks:
        print(f"- {risk}")
else:
    print("\nNo manager plan returned in state.")

print("\n=== GENERATED FILES ===")
if result.get("generated_files"):
    for path, content in result["generated_files"].items():
        print(f"\n--- {path} ---")
        print(content)

print("\n=== PROJECT ROOT ===")
print(result.get("project_root"))

print("\n=== TEST RESULTS ===")
print(result.get("test_results"))

print("\n=== REVIEW RESULTS ===")
print(result.get("review"))

print("\n=== FINAL STATUS ===")
print(result.get("status"))

print(f"\nReview Attempts: {result.get('review_attempts', 0)}")
print(f"Debug Attempts: {result.get('debug_attempts', 0)}")