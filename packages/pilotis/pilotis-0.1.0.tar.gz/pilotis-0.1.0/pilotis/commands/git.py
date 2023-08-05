from enum import Enum
from os import path
from pathlib import Path
from typing import Dict
from click import UsageError

import click
import inquirer

from pilotis.commands.init import OPTION_PROJECT_SLUG
from pilotis.commands.copier_utils import populate_and_copy
from pilotis.commands.shell_utils import call_shell
from pilotis.domain.pilotis_project_config import is_pilotis_project, NOT_A_PILOTIS_DIRECTORY_ERROR_MESSAGE

OPTION_PROVIDER = 'git_provider'
OPTION_ORGANIZATION = 'git_organization'
OPTION_GITLAB_GROUP = 'gitlab_group'
GITLAB_CI_FILE_NAME = ".gitlab-ci.yml"

_current_directory_path = Path(path.realpath(__file__)).parent
_templates_dir = _current_directory_path.parent.parent / 'templates'

GITLAB_DOC_HOSTING_HELP_PAGE = "https://docs.gitlab.com/ee/user/project/pages/#how-it-works"
GITHUB_DOC_HOSTING_HELP_PATH = "https://pages.github.com/"


class GitProvider(Enum):
    GITHUB = "Github"
    GITLAB = "Gitlab"


@click.command("git",
               short_help="Version with Git & create remote.",
               help="Version with Git & create remote on selected provider (Github, Gitlab).")
@click.option('--project-dir',
              type=click.Path(exists=True, file_okay=False, resolve_path=True),
              default='.',
              callback=lambda _, __, value: Path(value),
              help="Directory containing the project")
@click.option('--skip-install',
              type=bool,
              default=False,
              is_flag=True,
              help="Skip post installation scripts")
def git_command(project_dir: Path, skip_install: bool) -> None:
    if not is_pilotis_project(project_dir):
        raise UsageError(NOT_A_PILOTIS_DIRECTORY_ERROR_MESSAGE)

    substitution_data = _git_substitution_data(project_dir)
    generate(project_dir, substitution_data, skip_install)


def generate(project_dir: Path, substitution_data: Dict[str, str], skip_install: bool = False) -> None:
    _write_files(project_dir, substitution_data)
    _initialize_git_repository(project_dir)

    if not skip_install:
        _post_install_scripts(project_dir, substitution_data)

    _display_doc_hosting_help(substitution_data)


def _initialize_git_repository(project_dir: Path) -> None:
    call_shell("git init", project_dir)
    call_shell("git add .", project_dir)
    call_shell("git commit -m 'Init commit'", project_dir)


def _git_substitution_data(project_dir: Path) -> Dict[str, str]:
    project_slug = project_dir.name

    questions = [
        inquirer.List(
            OPTION_PROVIDER,
            message="Git provider?",
            choices=[provider.value for provider in GitProvider]
        ),
        inquirer.Text(
            OPTION_ORGANIZATION,
            message="Gitlab Organization?",
            ignore=lambda previous_answers: previous_answers[OPTION_PROVIDER] != GitProvider.GITLAB.value
        ),
        inquirer.Text(
            OPTION_GITLAB_GROUP,
            message="Gitlab Group?",
            ignore=lambda previous_answers: previous_answers[OPTION_PROVIDER] != GitProvider.GITLAB.value
        ),
        inquirer.Text(
            OPTION_ORGANIZATION,
            message="Github Organization?",
            ignore=lambda previous_answers: previous_answers[OPTION_PROVIDER] != GitProvider.GITHUB.value
        )
    ]

    answers = inquirer.prompt(questions)

    return {
        OPTION_PROJECT_SLUG: project_slug,
        OPTION_PROVIDER: answers[OPTION_PROVIDER],
        OPTION_ORGANIZATION: answers[OPTION_ORGANIZATION],
        OPTION_GITLAB_GROUP: answers[OPTION_GITLAB_GROUP]
    }


def _write_files(project_dir: Path, substitution_data: Dict[str, str]) -> None:
    git_templates_path = _templates_dir / "git"

    git_common_template_path = git_templates_path / "commons"
    populate_and_copy(git_common_template_path, project_dir, substitution_data)

    git_provider_template_path = git_templates_path / substitution_data[OPTION_PROVIDER].lower()
    populate_and_copy(git_provider_template_path, project_dir, substitution_data)


def _post_install_scripts(project_dir: Path, substitution_data: Dict[str, str]) -> None:
    remote = _gitlab_remote(substitution_data) \
        if substitution_data[OPTION_PROVIDER] == GitProvider.GITLAB.value \
        else _github_remote(substitution_data)
    call_shell(f'git push -u "{remote}" master', project_dir)


def _gitlab_remote(substitution_data: Dict[str, str]) -> str:
    organization = substitution_data[OPTION_ORGANIZATION]
    group = substitution_data[OPTION_GITLAB_GROUP]
    project_slug = substitution_data[OPTION_PROJECT_SLUG]
    return f'git@gitlab.com:{organization}/{group}/{project_slug}.git'


def _github_remote(substitution_data: Dict[str, str]) -> str:
    organization = substitution_data[OPTION_ORGANIZATION]
    project_slug = substitution_data[OPTION_PROJECT_SLUG]
    return f"git@github.com:{organization}/{project_slug}.git"


def _display_doc_hosting_help(substitution_data: Dict[str, str]):
    doc_hosting_help_page = GITLAB_DOC_HOSTING_HELP_PAGE \
        if substitution_data[OPTION_PROVIDER] == GitProvider.GITLAB.value \
        else GITHUB_DOC_HOSTING_HELP_PATH

    click.echo(f"Documentation hosting is not implemented yet. "
               f"You may find documentation on how to do it on {doc_hosting_help_page}")
