from typing import Union
import json

from langchain_ollama import ChatOllama

from agents.schemas import DevelopmentPlan, ManagerPlan, ResearchResult


llm = ChatOllama(
    model="gemma4:31b-cloud",
    temperature=0,
)


RESEARCHER_PROMPT = """
You are the Researcher Agent in an AI software development team.

Your job is to analyze the development plan and provide useful technical
research for the Architect.

You are NOT responsible for writing code.

Analyze:

DEVELOPMENT PLAN:
{plan}

Return ONLY valid JSON in this exact structure:

{{
    "findings": [
        "finding 1",
        "finding 2"
    ],
    "recommendations": [
        "recommendation 1",
        "recommendation 2"
    ],
    "technologies": [
        "technology 1",
        "technology 2"
    ],
    "risks": [
        "risk 1",
        "risk 2"
    ]
}}

Do not use Markdown.
Do not add explanations outside the JSON.
"""


def research_project(plan: Union[ManagerPlan, str, dict]) -> ResearchResult:
    if isinstance(plan, ManagerPlan):
        plan_json = plan.model_dump_json(indent=2)
    else:
        plan_json = json.dumps(plan)

    prompt = RESEARCHER_PROMPT.format(
        plan=plan_json
    )

    response = llm.invoke(prompt)

    try:
        data = json.loads(response.content)

        return ResearchResult.model_validate(data)

    except (json.JSONDecodeError, ValueError) as error:
        print("Researcher returned invalid structured output.")
        print("Raw response:")
        print(response.content)

        raise error