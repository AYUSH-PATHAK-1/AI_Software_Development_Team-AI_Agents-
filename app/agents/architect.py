import json

from langchain_ollama import ChatOllama

from agents.schemas import DevelopmentPlan, ArchitecturePlan, ResearchResult


llm = ChatOllama(
    model="gemma4:31b-cloud",
    temperature=0,
)


ARCHITECT_PROMPT = """
You are a senior software architect.

You will receive a development plan created by another AI agent.

Your job is to design the technical architecture for implementing that plan.

Return ONLY valid JSON.

Do NOT use Markdown.
Do NOT use code fences.
Do NOT include explanations outside the JSON.

The JSON must have exactly this structure:

{{
    "architecture": "overall architecture description",
    "components": [
        "component 1",
        "component 2"
    ],
    "files": [
        "file1.py",
        "file2.py"
    ],
    "data_flow": "description of how data moves through the system",
    "technical_decisions": [
        "decision 1",
        "decision 2"
    ]
}}

Development plan:

{plan}

RESEARCH RESULTS:

{research}

Use the research findings and recommendations when making architectural
decisions.Return ONLY valid JSON.

Keep the architecture practical.
Do not add unnecessary complexity.
"""


def design_architecture(plan: DevelopmentPlan, research: ResearchResult) -> ArchitecturePlan:

    plan_json = plan.model_dump_json(indent=2)
    research_json = research.model_dump_json(indent=2)

    prompt = ARCHITECT_PROMPT.format(
        plan=plan_json,
        research=research_json
    )

    response = llm.invoke(prompt)

    try:
        data = json.loads(response.content)

        return ArchitecturePlan.model_validate(data)

    except (json.JSONDecodeError, ValueError) as error:
        print("Architect returned invalid structured output.")
        print("Raw response:")
        print(response.content)

        raise error