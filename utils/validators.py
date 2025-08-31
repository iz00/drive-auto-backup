from collections.abc import Callable
from pathlib import Path
from re import fullmatch, search as regex_search
from time import strftime, strptime

from email_validator import EmailNotValidError, validate_email


DEFAULT_DRIVE_FOLDER = "root"
DEFAULT_BACKUP_TIME = "12:00"


def validate_and_get_absolute_local_path(path: str) -> str:
    if path and Path(path).exists():
        return str(Path(path).expanduser().resolve())

    raise ValueError("Invalid local path.")


def validate_and_get_drive_folder_id(drive_folder: str) -> str:
    drive_folder = drive_folder.replace(" ", "")

    if not drive_folder or drive_folder.lower() in ("/", "root", "home"):
        return DEFAULT_DRIVE_FOLDER

    if match := regex_search(r"(?:folders/|id=)(?P<id>[\w\-]+)", drive_folder):
        return match.group("id")

    if fullmatch(r"[\w\-]+", drive_folder):
        return drive_folder

    raise ValueError("Invalid Google Drive folder ID.")


def validate_and_get_drive_account_email(email: str) -> str:
    email = email.replace(" ", "")

    try:
        return validate_email(email).normalized

    except EmailNotValidError as error:
        raise ValueError(f"Invalid email account. {error}")


def validate_and_get_frequency(frequency: str) -> str:
    frequency = frequency.replace(" ", "")

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


def validate_and_get_time(time: str) -> str:
    time = time.replace(" ", "")

    if not time:
        return DEFAULT_BACKUP_TIME

    try:
        return strftime("%H:%M", strptime(time, "%H:%M"))

    except ValueError:
        raise ValueError("Invalid time format (expected HH:MM in 24-hour format).")


CONFIGS_VALIDATORS: dict[str : Callable[[str], str]] = {
    "local_path": validate_and_get_absolute_local_path,
    "drive_folder": validate_and_get_drive_folder_id,
    "drive_account": validate_and_get_drive_account_email,
    "frequency": validate_and_get_frequency,
    "time": validate_and_get_time,
}


def validate_configs(args: dict) -> dict:
    """
    Validate a dict of configs, returning only valid entries.
    Invalid values are reported and skipped.
    """
    valid_configs = {}

    for config, value in args.items():
        validator: Callable[[str], str] = CONFIGS_VALIDATORS[config]

        try:
            valid_configs[config] = validator(value)
        except ValueError as error:
            print(error)

    return valid_configs
