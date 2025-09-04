from collections.abc import Callable

from utils.backup_utils import format_config_label
from utils.config_setup import *
from utils.validators import CONFIGS_VALIDATORS


def add_handler(args: dict) -> None:
    create_config_file()

    try:
        total_configs = load_config()
    except ValueError as error:
        print(error)
        return

    fill_empty_values(args, get_default_configs(total_configs))

    for config in args.keys():
        args[config] = prompt_and_validate(config, args[config])

    if add_backup_to_config_file(args, total_configs):
        print("New backup succesfully added to config.json.")


def fill_empty_values(target: dict, source: dict) -> None:
    """
    Replace None or empty string values in `target`
    with values from `source`, when keys match.
    """
    for key, value in source.items():
        if target.get(key) is None and value:
            target[key] = value


def prompt_and_validate(config: str, value: str | None) -> str:
    """
    Prompt the user for a config value (if not present) and validate/parse it.
    Keeps asking until the input is valid.
    """
    validator: Callable[[str], str] = CONFIGS_VALIDATORS[config]

    while True:
        value: str = value or input(f"{format_config_label(config)}: ")
        try:
            return validator(value)
        except ValueError as error:
            print(error)
            # Force re-prompt
            value = None


def get_next_backup_id(backups: list[dict]) -> int:
    if not backups:
        return 0

    return max(backup.get("id", -1) for backup in backups) + 1


def add_backup_to_config_file(backup: dict, total_configs: dict) -> bool:
    new_backup_id = get_next_backup_id(total_configs["backups"])

    new_backup = {
        "id": new_backup_id,
        **backup,
        "last_backup": None,
        "scheduled": False,
    }

    total_configs["backups"].append(new_backup)

    save_config_to_file(total_configs)

    return True
