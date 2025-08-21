from pathlib import Path
from re import fullmatch, search as regex_search

from email_validator import EmailNotValidError, validate_email


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


def validate_and_get_drive_account_email(email: str) -> str:
    try:
        return validate_email(email).normalized

    except EmailNotValidError as error:
        raise ValueError(f"Invalid email account. {error}")


def validate_and_get_frequency(frequency: str) -> str:
    if not (
        match := regex_search(
            r"(?P<quantity>\d+)(?P<unit>m(?:inutes)?|h(?:ours)?|d(?:ays)?|w(?:eeks)?)",
            frequency.lower(),
        )
    ):
        raise ValueError(
            "Invalid frequency format (expected like '10m', '2h', '3d', '1w')."
        )

    if (quantity := int(match.group("quantity"))) <= 0:
        raise ValueError("Invalid frequency (expected positive number).")

    return f"{quantity}{match.group('unit')[0]}"
