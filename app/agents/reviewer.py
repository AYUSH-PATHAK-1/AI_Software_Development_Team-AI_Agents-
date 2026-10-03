import json

from langchain_ollama import ChatOllama

from agents.schemas import ReviewResult


llm = ChatOllama(
    model="gemma4:31b-cloud",
    temperature=0,
)


REVIEWER_PROMPT = """
You are the Reviewer Agent in an AI software development team.

Your responsibility is to perform a strict final review of the generated
software.

Evaluate the project in this order:

1. USER REQUIREMENTS
   Check whether the generated project satisfies the original request.

2. DEVELOPMENT PLAN
   Check whether the implementation follows the development plan.

3. ARCHITECTURE
   Check whether the generated files actually implement the proposed
   architecture and technical decisions.

4. GENERATED CODE
   Look for missing functionality, incorrect behavior, poor validation,
   obvious bugs, and inconsistencies.

5. TEST RESULTS
   Consider the test results, but remember that syntax checks alone do
   NOT prove that the application works correctly.

6. CROSS-LAYER CONSISTENCY
   Compare:
   
   USER REQUEST
       ↓
   DEVELOPMENT PLAN
       ↓
   RESEARCH
       ↓
   ARCHITECTURE
       ↓
   GENERATED CODE

   Important decisions should remain consistent through these layers.

Do not approve a project merely because the code compiles.

If an important problem exists, set approved to false.

For every issue provide:
- category
- severity
- description
- expected

Possible categories:
- requirement
- plan
- architecture
- implementation
- testing
- consistency

Possible severities:
- low
- medium
- high
- critical

USER REQUEST:
{user_request}

DEVELOPMENT PLAN:
{development_plan}

RESEARCH:
{research}

ARCHITECTURE:
{architecture}

GENERATED FILES:
{generated_files}

TEST RESULTS:
{test_results}

Return ONLY valid JSON:

{{
    "approved": true,
    "issues": [],
    "summary": "Short review summary."
}}
"""


def review_project(
    user_request: str,
    development_plan,
    research,
    architecture_plan,
    generated_files: dict[str, str],
    test_results: str,
) -> ReviewResult:

    development_plan_json = development_plan.model_dump_json(indent=2)
    architecture_json = architecture_plan.model_dump_json(indent=2)


    generated_files_json = json.dumps(
        generated_files,
        indent=2
    )


    prompt = REVIEWER_PROMPT.format(
        user_request=user_request,
        development_plan=development_plan_json,
        research=research.model_dump_json(indent=2),
        architecture=architecture_json,
        generated_files=generated_files_json,
        test_results=test_results,
    )

    response = llm.invoke(prompt)

    content = response.content

    if not isinstance(content, str):
        raise ValueError("Reviewer returned an unexpected response format.")

    try:
     if content.startswith("```"):
        content = content.strip()
        content = content.removeprefix("```json")
        content = content.removeprefix("```")
        content = content.removesuffix("```")
        content = content.strip()
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Reviewer returned invalid JSON:\n{content}"
        ) from exc

    return ReviewResult.model_validate(data)