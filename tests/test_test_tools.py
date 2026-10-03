# print("TEST TOOL IS WORKING")

# x = 10
# y = 20

# assert x + y == 30

# print("ASSERTION PASSED")

from pathlib import Path

from app.tools.test_tools import check_python_files


project_root = Path("tests")

result = check_python_files(project_root)

print(result)