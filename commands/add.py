import json
from collections.abc import Callable

from utils.config_setup import create_config_file
from utils.validators import CONFIGS_VALIDATORS


def add_handler(args: dict) -> None:
    create_config_file()

    default_configs = get_default_configs()
    fill_empty_values(args, default_configs)

    for config in args.keys():
        args[config] = prompt_and_validate(config, args[config])

    if add_backup_to_config_file(args):
        print("New backup succesfully added to config.json.")


def get_default_configs() -> dict:
    try:
        with open("config.json") as config_file:
            configs: dict = json.load(config_file)

            return {
                "drive_account": configs.get("default_drive_account"),
                "frequency": configs.get("default_frequency"),
                "time": configs.get("default_time"),
            }
    except OSError:
        return {}


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
        value: str = value or input(f"{config.replace('_', ' ').title()}: ")
        try:
            return validator(value.replace(" ", ""))
        except ValueError as error:
            print(error)
            # Force re-prompt
            value = None


def get_all_configs() -> dict:
    with open("config.json") as config_file:
        return json.load(config_file)


def get_next_backup_id(backups: list[dict]) -> int:
    if not backups:
        return 0

    return max(backup.get("id", -1) for backup in backups) + 1


def add_backup_to_config_file(configs: dict) -> bool:
    try:
        total_configs = get_all_configs()
    except OSError:
        print("Error: config.json not found.")
        return False

    try:
        new_backup_id = get_next_backup_id(total_configs["backups"])
    except KeyError:
        print('Error: config.json is malformed (missing "backups" array).')
        return False

    new_backup_configs = {
        "id": new_backup_id,
        **configs,
        "last_backup": None,
        "scheduled": False,
    }

    total_configs["backups"].append(new_backup_configs)

    with open("config.json", "w") as config_file:
        json.dump(total_configs, config_file, ensure_ascii=False, indent=4)

    return True
