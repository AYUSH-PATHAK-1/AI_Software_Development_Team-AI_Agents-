import os
import shutil
from pathlib import Path


def save_project_files(project_dir: str, files: dict[str, str]):
    """Writes project files while preserving virtual environments or hidden config folders."""
    os.makedirs(project_dir, exist_ok=True)

    for relative_path, content in files.items():
        file_path = os.path.join(project_dir, relative_path)

        # Ensure parent directories exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)


def clean_project_code_only(project_dir: Path):
    """Removes source code files while keeping .venv intact."""
    if not project_dir.exists():
        return

    for item in project_dir.iterdir():
        # Never delete the virtual environment
        if item.name == ".venv":
            continue

        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def write_project_files(
    files: dict[str, str],
    project_name: str = "generated_project",
) -> Path:
    project_root = (Path("generated_projects") / project_name).resolve()

    # Clean only source files while preserving .venv
    clean_project_code_only(project_root)

    # Ensure project root exists
    project_root.mkdir(parents=True, exist_ok=True)

    for file_path, content in files.items():
        path = (project_root / file_path).resolve()

        # Prevent directory traversal attacks
        try:
            path.relative_to(project_root)
        except ValueError:
            raise ValueError(f"Unsafe file path: {file_path}")

        path.parent.mkdir(parents=True, exist_ok=True)

        # Unescape escaped string literals from raw LLM outputs
        cleaned_content = (
            content.replace("\\n", "\n")
            .replace('\\"', '"')
            .replace("\\\\", "\\")
        )
        path.write_text(cleaned_content, encoding="utf-8")

    return project_root