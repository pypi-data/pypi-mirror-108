from dataclasses import dataclass


@dataclass
class Option:
    name: str
    help_message: str


BACKEND = Option("--backend", "Which filesystem backend to use (local or S3)")
BUCKET_NAME = Option("--bucket-name", "S3 bucket name where data is stored when using S3 backend")
WORK_DIR = Option("--work-dir", "Working directory where data is stored when using local backend")
