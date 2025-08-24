import json

from utils.config_setup import create_config_file


def add_handler(args: dict) -> None:
    create_config_file()

    default_configs = get_default_configs()
    fill_empty_values(args, default_configs)


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
