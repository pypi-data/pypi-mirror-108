import os
from os import path
from pathlib import Path
from typing import Set, Dict
import yaml

import click
import inquirer
from click import UsageError

from pilotis.commands.copier_utils import populate_and_copy
from pilotis.commands.init import OPTION_PROJECT_SLUG, slugify
from pilotis.commands.shell_utils import call_shell
from pilotis.domain.pilotis_project_config import is_pilotis_project, NOT_A_PILOTIS_DIRECTORY_ERROR_MESSAGE
from pilotis.domain.python_project_config import PYTHON_PROJECT_DIRECTORY_NAME, PoetryDependencyManager, GitDependency, \
    PypiDependency


_current_directory_path = Path(path.realpath(__file__)).parent
_templates_dir = _current_directory_path.parent.parent / 'templates'
_infra_templates_path = _templates_dir / "aws"

MANDATORY_ENVIRONMENT_VARIABLES: Set[str] = {"AWS_ACCESS_KEY_ID", "AWS_DEFAULT_REGION", "AWS_SECRET_ACCESS_KEY"}
MISSING_ENV_VAR_ERROR_MESSAGE = f"Missing AWS environment variable(s) in {MANDATORY_ENVIRONMENT_VARIABLES}"
OPTION_AWS_DATA_BUCKET_NAME = "aws_data_bucket_name"
OPTION_AWS_TERRAFORM_BUCKET_NAME = "aws_terraform_bucket_name"
OPTION_AWS_TERRAFORM_BUCKET_DIRECTORY = "aws_terraform_bucket_directory"

_PILOTIS_IO_ASW = GitDependency(
    name='pilotis-io-aws',
    repo='git@gitlab.com:ekinox-io/ekinox-libraries/pilotis-io-aws.git',
    branch='master',
)
_BOTO_3 = PypiDependency(
    name='boto3',
    version='^1.10.39',
)
_S3FS = PypiDependency(
    name='s3fs',
    version='^0.4.0',
)

MKDOCS_CONFIG_FILE_NAME = 'mkdocs.yml'
AWS_DATA_STORAGE_DOC_SECTION = {'AWS Data Storage': 'aws-data-storage.md'}


@click.command("aws", help="Use AWS as a technical backend")
@click.option("--project-dir",
              help="Directory containing the project",
              type=click.Path(file_okay=False, resolve_path=True),
              callback=lambda _, __, value: Path(value),
              default='.')
@click.option("--skip-install",
              help="Skip post installation scripts",
              is_flag=True)
def infra_command(project_dir: Path, skip_install: bool) -> None:
    click.echo(f"Generating AWS on {slugify(project_dir.name)}")

    if not is_pilotis_project(project_dir):
        raise UsageError(NOT_A_PILOTIS_DIRECTORY_ERROR_MESSAGE)
    if some_mandatory_variables_are_missing():
        raise UsageError(MISSING_ENV_VAR_ERROR_MESSAGE)

    substitution_data = _aws_substitution_data(project_dir)
    generate_aws(project_dir, substitution_data, skip_install)


def some_mandatory_variables_are_missing() -> bool:
    environment_variables = os.environ.keys()
    return not MANDATORY_ENVIRONMENT_VARIABLES.issubset(environment_variables)


def generate_aws(project_dir: Path, substitution_data: Dict[str, str], skip_install: bool) -> None:
    populate_and_copy(_infra_templates_path, project_dir, substitution_data)

    python_project_directory_path = project_dir / PYTHON_PROJECT_DIRECTORY_NAME
    poetry_dependency_manager = PoetryDependencyManager(python_project_directory_path)
    poetry_dependency_manager.add_git_dependency(_PILOTIS_IO_ASW)
    poetry_dependency_manager.add_pypi_dependency(_BOTO_3)
    poetry_dependency_manager.add_pypi_dependency(_S3FS)

    _update_doc_site(project_dir)

    if not skip_install:
        _create_aws_infrastructure(project_dir)


def _create_aws_infrastructure(project_dir):
    infrastructure_dir = project_dir / "infrastructure"
    call_shell("terraform init", infrastructure_dir)
    call_shell("terraform apply -auto-approve", infrastructure_dir)


def _update_doc_site(project_dir):
    with open(project_dir / PYTHON_PROJECT_DIRECTORY_NAME / MKDOCS_CONFIG_FILE_NAME, 'r') as mkdocs_config_stream:
        mkdocs_config = yaml.load(mkdocs_config_stream)
    mkdocs_config['nav'].append(AWS_DATA_STORAGE_DOC_SECTION)
    with open(project_dir / PYTHON_PROJECT_DIRECTORY_NAME / MKDOCS_CONFIG_FILE_NAME, 'w') as mkdocs_config_stream:
        yaml.safe_dump(mkdocs_config, mkdocs_config_stream, default_flow_style=False)


def _aws_substitution_data(project_dir: Path) -> Dict[str, str]:
    project_slug = slugify(project_dir.name)

    questions = [
        inquirer.Text(
            OPTION_AWS_TERRAFORM_BUCKET_NAME,
            message="Existing AWS bucket name to store Terraform state files?",
        ),
        inquirer.Text(
            OPTION_AWS_TERRAFORM_BUCKET_DIRECTORY,
            message=f"Subdirectory in terraform state files bucket?",
            default=project_dir.name
        ),
        inquirer.Text(
            OPTION_AWS_DATA_BUCKET_NAME,
            message="AWS bucket name where data will be stored",
            default=f'{project_dir.name}-data'
        )
    ]

    answers = inquirer.prompt(questions)

    return {
        OPTION_PROJECT_SLUG: project_slug,
        OPTION_AWS_DATA_BUCKET_NAME: answers[OPTION_AWS_DATA_BUCKET_NAME],
        OPTION_AWS_TERRAFORM_BUCKET_NAME: answers[OPTION_AWS_TERRAFORM_BUCKET_NAME],
        OPTION_AWS_TERRAFORM_BUCKET_DIRECTORY: answers[OPTION_AWS_TERRAFORM_BUCKET_DIRECTORY]
    }
