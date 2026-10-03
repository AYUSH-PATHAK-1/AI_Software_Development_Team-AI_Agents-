# import json

# from langchain_ollama import ChatOllama

# from agents.schemas import DevelopmentPlan, GeneratedProject,ArchitecturePlan


# llm = ChatOllama(
#     model="gemma4:31b-cloud",
#     temperature=0,
# )


# CODER_PROMPT = """
# You are an expert software developer.

# You will receive a software development plan from another AI agent.

# Your job is to implement that plan.

# Return ONLY valid JSON.

# Do NOT use Markdown.
# Do NOT use code fences.
# Do NOT include explanations outside the JSON.

# The JSON must have exactly this structure:

# {{
#     "files": [
#         {{
#             "path": "relative/path/to/file.py",
#             "content": "complete file contents"
#         }}
#     ]
# }}

# Important rules:

# 1. Generate complete files, not code snippets.
# 2. Every file must have a relative path.
# 3. Include all files necessary for the requested implementation.
# 4. Code should be internally consistent.
# 5. Follow the development plan.
# 6. Do not leave TODO placeholders for core functionality.
# 7. Make sure generated Python code has correct indentation.
# 8. Make sure all generated imports are internally consistent.
# 9. Include tests cases when appropriate.
# 10. Do not include files outside the requested project.

# Development plan:

# {plan}

# Architecture plan:

# {architecture}

# Previous reviewer feedback:

# {review_feedback}

# If reviewer feedback exists:
# - Fix every valid issue identified by the reviewer.
# - Preserve functionality that is already correct.
# - Return the complete corrected project files.

# If there is no previous review, implement the development plan normally.
# """


# def create_project(plan: DevelopmentPlan, architecture: ArchitecturePlan, review=None) -> GeneratedProject:
#     plan_json = plan.model_dump_json(indent=2)
#     architecture_json = architecture.model_dump_json(indent=2)
#     review_feedback = None

    
#     if review is not None:
#      review_feedback = review.model_dump_json(indent=2)
    
#     prompt = CODER_PROMPT.format(
#         plan=plan_json,
#         architecture=architecture_json,        
#         review_feedback=review_feedback,
#     )
    
#     response = llm.invoke(prompt)

#     try:
#         data = json.loads(response.content)

#         return GeneratedProject.model_validate(data)

#     except (json.JSONDecodeError, ValueError) as error:
#         print("Coder returned invalid structured output.")
#         print("Raw response:")
#         print(response.content)

#         raise error



import json
import re
from langchain_ollama import ChatOllama
from agents.schemas import DevelopmentPlan, GeneratedProject, ArchitecturePlan

llm = ChatOllama(
    model="gpt-oss:120b-cloud",
    temperature=0,
)

CODER_PROMPT = """
You are an expert software developer.

Implement ALL components described in the Architecture plan.

STRICT GENERATION RULES:
1. You MUST generate ALL files specified in the Architecture plan (e.g., core/database.py, models/task_model.py, schemas/task_schema.py, services/task_service.py, api/routes/tasks.py, main.py, requirements.txt, tests/test_tasks.py).
2. Do NOT omit implementation files or leave skeleton imports.
3. Every file must be complete, runnable, and free of placeholder code.
4. Ensure import statements across files match the folder directory tree.
5. MUST ALWAYS generate unit test files inside a `tests/` directory (e.g., `tests/test_tasks.py`) using `pytest` and `httpx`.
6. MUST ALWAYS include `pytest`, `pytest-asyncio`, `httpx`, `fastapi`, and `uvicorn` in `requirements.txt`.

Return ONLY a valid JSON object. Do not include markdown code blocks or conversational text.

The JSON structure must match this EXACT schema:
{{
    "files": [
        {{
            "path": "relative/path/to/file.py",
            "content": "complete file contents here"
        }}
    ]
}}

DEVELOPMENT PLAN:
{plan}

ARCHITECTURE PLAN:
{architecture}

PREVIOUS REVIEWER FEEDBACK:
{review_feedback}

If reviewer feedback exists:
- Fix every valid issue identified by the reviewer.
- Preserve functionality that is already correct.
- Return the complete corrected project files.
"""

def _clean_and_parse_json(content: str) -> dict:
    """Extracts and parses JSON safely, stripping markdown wrappers or preambles."""
    # Attempt direct json load first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Extract standard json block enclosed in brackets
    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1:
        clean_str = content[start : end + 1]
        return json.loads(clean_str)

    raise ValueError("Failed to locate valid JSON block in model response.")


def create_project(plan: DevelopmentPlan, architecture: ArchitecturePlan, review=None) -> GeneratedProject:
    plan_json = plan.model_dump_json(indent=2)
    architecture_json = architecture.model_dump_json(indent=2)
    
    if review is not None:
        review_feedback = review.model_dump_json(indent=2)
    else:
        review_feedback = "No previous reviewer feedback."

    prompt = CODER_PROMPT.format(
        plan=plan_json,
        architecture=architecture_json,        
        review_feedback=review_feedback,
    )
    
    response = llm.invoke(prompt)

    try:
        data = _clean_and_parse_json(response.content)
        return GeneratedProject.model_validate(data)

    except Exception as error:
        print("Coder returned invalid structured output.")
        print("Raw response:")
        print(response.content)
        raise error