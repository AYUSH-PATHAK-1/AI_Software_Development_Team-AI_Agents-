import json
import re
from langchain_ollama import ChatOllama
from agents.schemas import GeneratedProject

llm = ChatOllama(
    model="gemma4:31b-cloud",
    temperature=0,
)

DEBUGGER_PROMPT = """
You are an expert software debugger.

You will receive:
1. The full set of files from a software project.
2. The results/errors from a test run.

Your job is to identify the problems, fix the code, and return ALL project files.

CRITICAL INSTRUCTIONS:
1. Return EVERY single project file in the final output—including files that did NOT have errors (e.g., database.py, requirements.txt, main.py).
2. If the test error reports a missing module (ModuleNotFoundError or ImportError), update or add `requirements.txt` containing the missing dependency (e.g., `httpx`, `pytest-asyncio`).
3. Ensure every file is complete and contains no placeholders like "# TODO".

Return ONLY valid JSON with this exact structure:
{{
    "files": [
        {{
            "path": "relative/path/to/file.py",
            "content": "complete file contents"
        }}
    ]
}}

GENERATED FILES:
{files}

TEST RESULTS:
{test_results}
"""

def _extract_files_from_response(raw_text: str) -> dict:
    """Parses JSON or markdown code blocks into a structured dictionary."""
    # Strategy 1: Try direct JSON parse
    try:
        start_idx = raw_text.find("{")
        end_idx = raw_text.rfind("}")
        if start_idx != -1 and end_idx != -1:
            json_str = raw_text[start_idx : end_idx + 1]
            return json.loads(json_str)
    except Exception:
        pass

    # Strategy 2: Extract code blocks if LLM responded with markdown ```python filename ... ```
    pattern = r"```(?:python)?\s*\n\s*#\s*([^\n]+)\n(.*?)```"
    matches = re.findall(pattern, raw_text, re.DOTALL)
    
    if matches:
        files = []
        for path, content in matches:
            files.append({"path": path.strip(), "content": content.strip()})
        return {"files": files}

    raise ValueError("Could not parse JSON or code blocks from Debugger response.")


def debug_project(
    generated_files: dict[str, str],
    test_results: str,
) -> GeneratedProject:
    files_json = json.dumps(generated_files, indent=2)

    prompt = DEBUGGER_PROMPT.format(
        files=files_json,
        test_results=test_results,
    )

    # Use standard LLM invoke instead of structured output parser
    response = llm.invoke(prompt)
    raw_content = str(response.content)

    try:
        data = _extract_files_from_response(raw_content)
        return GeneratedProject.model_validate(data)

    except Exception as error:
        print("Debugger returned invalid structured output.")
        print("Raw response:")
        print(raw_content)
        raise error