import json
from langchain_ollama import ChatOllama
from agents.schemas import ManagerPlan

llm = ChatOllama(
    model="gemma4:31b-cloud",
    temperature=0,
)

MANAGER_PROMPT = """
You are the Project Manager of an autonomous AI software development team.

Your job is to analyze the incoming user requirement, break it down into functional requirements, 
identify early project risks, and create a structured task breakdown for your team 
(Researcher, Architect, Coder, Tester, Reviewer).

Return ONLY valid JSON matching the exact schema below.
Do NOT use Markdown.
Do NOT use code fences.
Do NOT include explanations outside the JSON.

The JSON must have strictly this structure:

{{
    "project_name": "string",
    "summary": "string",
    "requirements": ["requirement 1", "requirement 2"],
    "tasks": [
        {{
            "task_id": 1,
            "title": "string",
            "description": "string",
            "assigned_agent": "string"
        }}
    ],
    "potential_risks": ["risk 1", "risk 2"]
}}

User Requirement:
{user_request}
"""

def create_manager_plan(user_request: str) -> ManagerPlan:
    prompt = MANAGER_PROMPT.format(user_request=user_request)
    response = llm.invoke(prompt)

    try:
        data = json.loads(response.content)
        return ManagerPlan.model_validate(data)
    except (json.JSONDecodeError, ValueError) as error:
        print("Manager returned invalid structured output.")
        print("Raw response:")
        print(response.content)
        raise error