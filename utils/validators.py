from pathlib import Path
from re import fullmatch, search as regex_search


DEFAULT_DRIVE_FOLDER = "root"


def validate_and_get_absolute_local_path(path: str) -> str:
    if path and Path(path).exists():
        return str(Path(path).expanduser().resolve())

    raise ValueError("Invalid local path.")


def validate_and_get_drive_folder_id(drive_folder: str) -> str:
    if not drive_folder or drive_folder.lower() in ("/", "root", "home"):
        return DEFAULT_DRIVE_FOLDER

    if match := regex_search(r"(?:folders/|id=)(?P<id>[\w\-]+)", drive_folder):
        return match.group("id")

    if fullmatch(r"[\w\-]+", drive_folder):
        return drive_folder

    raise ValueError("Invalid Google Drive folder ID.")
