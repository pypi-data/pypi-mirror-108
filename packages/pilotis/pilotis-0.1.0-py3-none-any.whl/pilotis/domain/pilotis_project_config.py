from pathlib import Path

PILOTIS_CONFIG_FILE_NAME = "pilotis.config"
NOT_A_PILOTIS_DIRECTORY_ERROR_MESSAGE = "This command should be run in a pilotis project directory"


def is_pilotis_project(directory: Path) -> bool:
    return (directory / PILOTIS_CONFIG_FILE_NAME).exists()


def init_config(project_parent_dir: Path, project_slug: str) -> None:
    (project_parent_dir / project_slug / PILOTIS_CONFIG_FILE_NAME).touch()
