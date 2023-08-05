from dataclasses import dataclass
from pathlib import Path

import toml
from toml import TomlPreserveInlineDictEncoder
from toml.decoder import InlineTableDict

PYTHON_PROJECT_DIRECTORY_NAME = 'python'
PYPROJECT_TOML_FILE_NAME = 'pyproject.toml'

PYPROJECT_TOOL_SECTION_NAME = 'tool'
PYPROJECT_POETRY_SECTION_NAME = 'poetry'
PYPROJECT_DEPENDENCIES_SECTION_NAME = 'dependencies'


@dataclass
class PypiDependency:
    name: str
    version: str


@dataclass
class GitDependency:
    name: str
    repo: str
    branch: str


class PoetryDependencyManager:
    def __init__(self, poetry_project_dir: Path, ):
        self.poetry_project_dir = poetry_project_dir
        self.poetry_toml_file = poetry_project_dir / PYPROJECT_TOML_FILE_NAME
        if not self.poetry_toml_file.exists():
            raise NoPyprojectException(self.poetry_project_dir)

    def add_pypi_dependency(self, dependency: PypiDependency) -> None:
        current_dependencies = toml.load(self.poetry_toml_file)

        current_dependencies[PYPROJECT_TOOL_SECTION_NAME][PYPROJECT_POETRY_SECTION_NAME][
            PYPROJECT_DEPENDENCIES_SECTION_NAME][dependency.name] = dependency.version

        with self.poetry_toml_file.open('w') as file_handle:
            toml.dump(current_dependencies, file_handle, encoder=TomlPreserveInlineDictEncoder())

    def add_git_dependency(self, dependency: GitDependency) -> None:
        class TomlInlineDict(dict, InlineTableDict):
            pass

        current_dependencies = toml.load(self.poetry_toml_file)
        current_dependencies[PYPROJECT_TOOL_SECTION_NAME][PYPROJECT_POETRY_SECTION_NAME][
            PYPROJECT_DEPENDENCIES_SECTION_NAME][dependency.name] = TomlInlineDict(
            {
                'git': dependency.repo,
                'branch': dependency.branch
            })

        with self.poetry_toml_file.open('w') as file_handle:
            toml.dump(current_dependencies, file_handle, encoder=TomlPreserveInlineDictEncoder())


class NoPyprojectException(Exception):
    def __init__(self, project_directory) -> None:
        self.message = f'No pyproject.toml found in target directory {project_directory}. ' \
                       f'Did you execute the init command in the same directory ?'
        super().__init__(self.message)
