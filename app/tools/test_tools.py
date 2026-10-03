# from pathlib import Path
# import py_compile


# def check_python_files(project_root: Path) -> str:
#     results = []
#     failed = False

#     python_files = list(project_root.rglob("*.py"))

#     if not python_files:
#         return "FAIL: No Python files found."

#     for file_path in python_files:
#         try:
#             py_compile.compile(
#                 str(file_path),
#                 doraise=True,
#             )

#             results.append(
#                 f"PASS: {file_path.relative_to(project_root)}"
#             )

#         except py_compile.PyCompileError as error:
#             failed = True

#             results.append(
#                 f"FAIL: {file_path.relative_to(project_root)}\n"
#                 f"{error}"
#             )

#     if failed:
#         return "TEST FAILED\n\n" + "\n".join(results)

#     return "TEST PASSED\n\n" + "\n".join(results)


# from pathlib import Path
# import py_compile
# import subprocess
# import sys


# def check_python_files(project_root: Path) -> str:
#     results = []
#     failed = False

#     python_files = list(project_root.rglob("*.py"))

#     if not python_files:
#         return "TEST FAILED\n\nFAIL: No Python files found."

#     # ---------------------------------------------------------
#     # 1. Syntax check
#     # ---------------------------------------------------------
#     for file_path in python_files:
#         try:
#             py_compile.compile(
#                 str(file_path),
#                 doraise=True,
#             )

#             results.append(
#                 f"PASS: {file_path.relative_to(project_root)}"
#             )

#         except py_compile.PyCompileError as error:
#             failed = True

#             results.append(
#                 f"FAIL: {file_path.relative_to(project_root)}\n"
#                 f"{error}"
#             )

#     # If syntax is broken, don't execute anything.
#     if failed:
#         return "TEST FAILED\n\n" + "\n".join(results)

#     # ---------------------------------------------------------
#     # 2. Find test files
#     # ---------------------------------------------------------
#     test_files = [
#         file_path
#         for file_path in python_files
#         if file_path.name.startswith("test_")
#         or file_path.name.endswith("_test.py")
#     ]

#     if not test_files:
#         results.append("INFO: No test files found. Syntax checks passed.")
#         return "TEST PASSED\n\n" + "\n".join(results)

#     # ---------------------------------------------------------
#     # 3. Execute test files
#     # ---------------------------------------------------------
#     for test_file in test_files:
#         try:
#             process = subprocess.run(
#                 [sys.executable,"-m", "pytest", str(test_file)],
#                 cwd=str(project_root),
#                 capture_output=True,
#                 text=True,
#                 timeout=30,
#             )

#             relative_path = test_file.relative_to(project_root)

#             if process.returncode == 0:
#                 results.append(
#                     f"PASS: {relative_path}\n"
#                     f"Output:\n{process.stdout.strip()}"
#                 )
#             else:
#                 failed = True

#                 results.append(
#                     f"FAIL: {relative_path}\n"
#                     f"Exit code: {process.returncode}\n"
#                     f"STDOUT:\n{process.stdout.strip()}\n"
#                     f"STDERR:\n{process.stderr.strip()}"
#                 )

#         except subprocess.TimeoutExpired:
#             failed = True

#             results.append(
#                 f"FAIL: {test_file.relative_to(project_root)}\n"
#                 "Test execution timed out after 30 seconds."
#             )

#         except Exception as error:
#             failed = True

#             results.append(
#                 f"FAIL: {test_file.relative_to(project_root)}\n"
#                 f"Execution error: {error}"
#             )

#     # ---------------------------------------------------------
#     # 4. Final result
#     # ---------------------------------------------------------
#     if failed:
#         return "TEST FAILED\n\n" + "\n".join(results)

#     return "TEST PASSED\n\n" + "\n".join(results)









# from pathlib import Path
# import py_compile
# import subprocess
# import sys


# def setup_virtual_environment(project_root: Path) -> Path:
#     """Creates a virtual environment inside the generated project and installs dependencies."""
#     venv_dir = project_root / ".venv"
    
#     # Determine the python and pip executables based on OS
#     if sys.platform == "win32":
#         python_executable = venv_dir / "Scripts" / "python.exe"
#         pip_executable = venv_dir / "Scripts" / "pip.exe"
#     else:
#         python_executable = venv_dir / "bin" / "python"
#         pip_executable = venv_dir / "bin" / "pip"

#     # Create .venv if it doesn't exist
#     if not venv_dir.exists():
#         subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)


#         # 2. Always ensure pytest (and pytest-asyncio/httpx if needed) are in the isolated env
#     subprocess.run(
#         [str(python_executable), "-m", "pip", "install", "pytest", "pytest-asyncio", "httpx"],
#         cwd=str(project_root),
#         capture_output=True,
#         text=True,
#         check=True,
#     )

#     # Install requirements.txt if present
#     requirements_file = project_root / "requirements.txt"
#     if requirements_file.exists():
#         subprocess.run(
#             [str(python_executable),"-m", "pip", "install", "-r", str(requirements_file)],
#             cwd=str(project_root),
#             capture_output=True,
#             text=True,
#             check=True
#         )

#     return python_executable


# def check_python_files(project_root: Path) -> str:
#     results = []
#     failed = False

#     python_files = list(project_root.rglob("*.py"))
#     # Exclude files inside .venv from syntax checks
#     python_files = [f for f in python_files if ".venv" not in f.parts]

#     if not python_files:
#         return "TEST FAILED\n\nFAIL: No Python files found."

#     # 1. Syntax check
#     for file_path in python_files:
#         try:
#             py_compile.compile(str(file_path), doraise=True)
#             results.append(f"PASS Syntax: {file_path.relative_to(project_root)}")
#         except py_compile.PyCompileError as error:
#             failed = True
#             results.append(f"FAIL Syntax: {file_path.relative_to(project_root)}\n{error}")

#     if failed:
#         return "TEST FAILED\n\n" + "\n".join(results)

#     # 2. Setup environment and install dynamic dependencies
#     try:
#         isolated_python = setup_virtual_environment(project_root)
#     except subprocess.CalledProcessError as env_error:
#         return f"TEST FAILED\n\nVirtual environment setup / dependency install failed:\n{env_error.stderr}"
#     except Exception as env_error:
#         return f"TEST FAILED\n\nVirtual environment setup failed: {env_error}"

#     # 3. Find and run test files using the isolated environment's Python
#     test_files = [
#         f for f in python_files 
#         if f.name.startswith("test_") or f.name.endswith("_test.py")
#     ]

#     if not test_files:
#         results.append("INFO: No test files found. Syntax checks passed.")
#         return "TEST PASSED\n\n" + "\n".join(results)

#     for test_file in test_files:
#         try:
#             process = subprocess.run(
#                 [str(isolated_python), "-m", "pytest", str(test_file)],
#                 cwd=str(project_root),
#                 capture_output=True,
#                 text=True,
#                 timeout=45,
#             )

#             relative_path = test_file.relative_to(project_root)

#             if process.returncode == 0:
#                 results.append(f"PASS Test: {relative_path}\nOutput:\n{process.stdout.strip()}")
#             else:
#                 failed = True
#                 results.append(
#                     f"FAIL Test: {relative_path}\n"
#                     f"Exit code: {process.returncode}\n"
#                     f"STDOUT:\n{process.stdout.strip()}\n"
#                     f"STDERR:\n{process.stderr.strip()}"
#                 )

#         except subprocess.TimeoutExpired:
#             failed = True
#             results.append(f"FAIL Test: {test_file.relative_to(project_root)}\nExecution timed out after 45s.")
#         except Exception as error:
#             failed = True
#             results.append(f"FAIL Test: {test_file.relative_to(project_root)}\nExecution error: {error}")

#     if failed:
#         return "TEST FAILED\n\n" + "\n".join(results)

#     return "TEST PASSED\n\n" + "\n".join(results)




import os
import py_compile
import subprocess
import sys
from pathlib import Path

def setup_virtual_environment(project_root: Path) -> Path:
    """Creates a persistent virtualenv, installs project dependencies and test tools."""
    venv_dir = project_root / ".venv"
    
    # 1. Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    
    # Resolve executable paths for Windows vs POSIX
    if os.name == "nt":
        pip_path = venv_dir / "Scripts" / "pip.exe"
        python_path = venv_dir / "Scripts" / "python.exe"
    else:
        pip_path = venv_dir / "bin" / "pip"
        python_path = venv_dir / "bin" / "python"

    # 2. Pre-install essential test runners
    testing_dependencies = ["pytest", "pytest-asyncio", "httpx", "fastapi"]
    subprocess.run([str(pip_path), "install", "--upgrade"] + testing_dependencies, check=True)

    # 3. Install project dependencies if requirements.txt exists
    req_file = project_root / "requirements.txt"
    if req_file.exists():
        subprocess.run([str(pip_path), "install", "-r", str(req_file)], check=True)

    return python_path


def check_python_files(project_root: Path) -> str:
    results = []
    failed = False

    # ---------------------------------------------------------
    # 1. Find Python files
    # ---------------------------------------------------------
    python_files = list(project_root.rglob("*.py"))
    python_files = [
        file_path for file_path in python_files if ".venv" not in file_path.parts
    ]

    if not python_files:
        return "TEST FAILED\n\nFAIL: No Python files found."

    # ---------------------------------------------------------
    # 2. Syntax check
    # ---------------------------------------------------------
    for file_path in python_files:
        try:
            py_compile.compile(str(file_path), doraise=True)
            results.append(f"PASS Syntax: {file_path.relative_to(project_root)}")
        except py_compile.PyCompileError as error:
            failed = True
            results.append(
                f"FAIL Syntax: {file_path.relative_to(project_root)}\n{error}"
            )

    if failed:
        return "TEST FAILED\n\n" + "\n".join(results)

    # ---------------------------------------------------------
    # 3. Create isolated environment
    # ---------------------------------------------------------
    try:
        isolated_python = setup_virtual_environment(project_root)
        results.append("PASS Environment: isolated virtual environment ready")
    except subprocess.CalledProcessError as error:
        return (
            "TEST FAILED\n\n"
            + "\n".join(results)
            + "\nFAIL Environment: dependency installation failed\n"
            f"Exit code: {error.returncode}\n"
            f"STDOUT:\n{error.stdout or ''}\n"
            f"STDERR:\n{error.stderr or ''}"
        )
    except Exception as error:
        return (
            "TEST FAILED\n\n"
            + "\n".join(results)
            + f"\nFAIL Environment: {error}"
        )

    # ---------------------------------------------------------
    # 4. Find test files
    # ---------------------------------------------------------
    test_files = [
        file_path
        for file_path in python_files
        if file_path.name.startswith("test_") or file_path.name.endswith("_test.py")
    ]

    if not test_files:
        results.append("INFO: No test files found. Syntax checks passed.")
        return "TEST PASSED\n\n" + "\n".join(results)

    # ---------------------------------------------------------
    # 5. Execute tests inside generated project's .venv
    # ---------------------------------------------------------
    # Prepare environment with PYTHONPATH set to project root for module imports
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)

    for test_file in test_files:
        try:
            process = subprocess.run(
                [
                    str(isolated_python),
                    "-m",
                    "pytest",
                    str(test_file),
                ],
                cwd=str(project_root),
                env=env,  # Enforces PYTHONPATH
                capture_output=True,
                text=True,
                timeout=45,
            )

            relative_path = test_file.relative_to(project_root)

            if process.returncode == 0:
                results.append(
                    f"PASS Test: {relative_path}\n"
                    f"Output:\n{process.stdout.strip()}"
                )
            else:
                failed = True
                results.append(
                    f"FAIL Test: {relative_path}\n"
                    f"Exit code: {process.returncode}\n"
                    f"STDOUT:\n{process.stdout.strip()}\n"
                    f"STDERR:\n{process.stderr.strip()}"
                )

        except subprocess.TimeoutExpired:
            failed = True
            results.append(
                f"FAIL Test: {test_file.relative_to(project_root)}\n"
                "Execution timed out after 45 seconds."
            )
        except Exception as error:
            failed = True
            results.append(
                f"FAIL Test: {test_file.relative_to(project_root)}\n"
                f"Execution error: {error}"
            )

    # ---------------------------------------------------------
    # 6. Final result
    # ---------------------------------------------------------
    if failed:
        return "TEST FAILED\n\n" + "\n".join(results)

    return "TEST PASSED\n\n" + "\n".join(results)