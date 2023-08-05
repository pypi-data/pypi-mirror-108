from pathlib import Path
from subprocess import call


def call_shell(command: str, working_dir: Path) -> int:
    return call(command, cwd=working_dir, shell=True)
