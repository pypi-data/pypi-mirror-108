from pathlib import Path
from typing import Dict

from copier import copy


def populate_and_copy(template_path: Path, project_dir: Path, templating_variables: Dict[str, str]) -> None:
    copy(
        str(template_path),
        project_dir,
        data=templating_variables,
        cleanup_on_error=False
    )
