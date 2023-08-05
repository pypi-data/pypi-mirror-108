import re
import stat
from os import path, chmod
from pathlib import Path
from typing import Dict

import click
import inquirer

from pilotis.commands.copier_utils import populate_and_copy
from pilotis.commands.shell_utils import call_shell
from pilotis.domain.pilotis_project_config import init_config

PYENV_CONFIG_BASH_FILE_NAME = "pyenv_config.bash"
CHECK_TOOLS_BASH_FILE_NAME = "check_tools.bash"

OPTION_PROJECT_NAME = 'project_name'
OPTION_PROJECT_SLUG = 'project_slug'
OPTION_PYTHON_PACKAGE_NAME = 'python_package_name'

SCRIPTS_DIR = Path("scripts")

_slug_forbidden_char = '[_ ]'
_current_directory_path = Path(path.realpath(__file__)).parent
_templates_dir = _current_directory_path.parent.parent / 'templates'
_main_templates_path = _templates_dir / 'init'


@click.command("init", help="Initialize project: generate base folders & files.")
@click.option('--project-parent-dir',
              type=click.Path(exists=True, file_okay=False, resolve_path=True),
              default='.',
              callback=lambda _, __, value: Path(value),
              help="Directory where the project will be created")
@click.option('--skip-install',
              type=bool,
              default=False,
              is_flag=True,
              help="Skip post installation scripts")
def init_command(project_parent_dir: Path, skip_install: bool) -> None:
    substitution_data = _init_substitution_data()
    generate(project_parent_dir, skip_install=skip_install, substitution_data=substitution_data)


def generate(project_parent_dir: Path, substitution_data: Dict[str, str] = None, skip_install: bool = False) -> None:
    _write_files(project_parent_dir, substitution_data)
    if not skip_install:
        _post_install_scripts(project_parent_dir, substitution_data)


def _init_substitution_data() -> Dict[str, str]:
    questions = [
        inquirer.Text(OPTION_PROJECT_NAME, message="Project name?")
    ]
    answers = inquirer.prompt(questions)

    project_name = answers[OPTION_PROJECT_NAME]
    project_slug = slugify(project_name)
    python_package_name = project_slug.replace('-', '_')

    return {
        OPTION_PROJECT_NAME: project_name,
        OPTION_PROJECT_SLUG: project_slug,
        OPTION_PYTHON_PACKAGE_NAME: python_package_name
    }


def slugify(project_name: str) -> str:
    lowered_name = project_name.lower()
    return re.sub(_slug_forbidden_char, '-', lowered_name)


def _post_install_scripts(project_parent_dir: Path, substitution_data: Dict[str, str]) -> None:
    call_shell("make setup-env", working_dir=project_parent_dir / substitution_data[OPTION_PROJECT_SLUG])


def _write_files(project_parent_dir: Path, substitution_data: Dict[str, str]) -> None:
    populate_and_copy(_main_templates_path, project_parent_dir, substitution_data)
    _make_env_scripts_executable(project_parent_dir, substitution_data)
    init_config(project_parent_dir, substitution_data[OPTION_PROJECT_SLUG])


def _make_env_scripts_executable(project_parent_dir: Path, substitution_data: Dict[str, str]) -> None:
    setup_env_script_path = project_parent_dir / substitution_data[OPTION_PROJECT_SLUG] / SCRIPTS_DIR
    chmod(setup_env_script_path / CHECK_TOOLS_BASH_FILE_NAME, stat.S_IXUSR | stat.S_IRUSR)
    chmod(setup_env_script_path / PYENV_CONFIG_BASH_FILE_NAME, stat.S_IXUSR | stat.S_IRUSR)
