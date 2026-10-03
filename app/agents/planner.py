import json

from langchain_ollama import ChatOllama

from agents.schemas import DevelopmentPlan


llm = ChatOllama(
    model="gemma4:31b-cloud",
    temperature=0,
)


PLANNER_PROMPT = """
You are a software development planner.

Convert the user's software request into a development plan.

You MUST return ONLY valid JSON.

Do NOT use Markdown.
Do NOT use code fences.
Do NOT include explanations before or after the JSON.

The JSON MUST have exactly these fields:

{{
    "requirements": ["requirement 1", "requirement 2"],
    "technical_approach": "description of technical approach",
    "files_needed": ["file1.py", "file2.py"],
    "implementation_steps": ["step 1", "step 2"]
}}

User request:

{request}
"""


def create_plan(request: str) -> DevelopmentPlan:
    prompt = PLANNER_PROMPT.format(request=request)

    response = llm.invoke(prompt)

    try:
        data = json.loads(response.content)
        return DevelopmentPlan.model_validate(data)

    except (json.JSONDecodeError, ValueError) as error:
        print("Planner returned invalid structured output.")
        print("Raw response:")
        print(response.content)

        raise error