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
    """Load config from `config_file` and validate its basic structure."""
    try:
        with Path(config_file).open("r", encoding="utf-8") as file:
            config: dict = json.load(file)

    except FileNotFoundError:
        raise ValueError(f"Config file {config_file} not found.")
    except json.JSONDecodeError as error:
        raise ValueError(f"Config file {config_file} is not valid JSON: {error}")

    backups: list[dict] = config.get("backups")

    if backups is None:
        raise ValueError('Config file is malformed: missing "backups" key.')
    if not isinstance(backups, list):
        raise ValueError('Config file is malformed: "backups" must be a list.')
    if not all(isinstance(backup, dict) for backup in backups):
        raise ValueError(
            'Config file is malformed: all elements in "backups" must be dictionaries.'
        )

    return config


def save_config_to_file(
    new_config: dict, config_file: str | Path = CONFIG_PATH
) -> None:
    with Path(config_file).open("w", encoding="utf-8") as file:
        json.dump(new_config, file, ensure_ascii=False, indent=4)


def get_default_configs(configs: dict) -> dict:
    return {
        "drive_account": configs.get("default_drive_account"),
        "frequency": configs.get("default_frequency"),
        "time": configs.get("default_time"),
    }
