import json

from pathlib import Path


CONFIG_PATH = Path("config.json")

INITIAL_CONFIG_DATA = {
    "default_drive_account": "",
    "default_frequency": "",
    "default_time": "",
    "backups": [],
}


def create_config_file(config_file: str | Path = CONFIG_PATH) -> bool:
    try:
        with Path(config_file).open("x", encoding="utf-8") as file:
            json.dump(INITIAL_CONFIG_DATA, file, indent=4, ensure_ascii=False)
            return True

    except FileExistsError:
        return False


def load_config(config_file: str | Path = CONFIG_PATH) -> dict:
    with Path(config_file).open("r", encoding="utf-8") as file:
        return json.load(file)


def save_config_to_file(
    new_config: dict, config_file: str | Path = CONFIG_PATH
) -> None:
    with Path(config_file).open("w", encoding="utf-8") as file:
        json.dump(new_config, file, ensure_ascii=False, indent=4)


def get_default_configs(config_file: str | Path = CONFIG_PATH) -> dict:
    try:
        configs = load_config(config_file)
        return {
            "drive_account": configs.get("default_drive_account"),
            "frequency": configs.get("default_frequency"),
            "time": configs.get("default_time"),
        }
    except OSError:
        return {}
