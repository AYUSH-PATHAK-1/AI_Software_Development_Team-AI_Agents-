from app.agents.debugger import debug_project


generated_files = {
    "main.py": """
def hello():
    print("Hello"

hello()
"""
}


test_results = """
TEST FAILED

FAIL: main.py

SyntaxError: '(' was never closed
"""


project = debug_project(
    generated_files,
    test_results,
)


for file in project.files:
    print(f"\n--- {file.path} ---")
    print(file.content)