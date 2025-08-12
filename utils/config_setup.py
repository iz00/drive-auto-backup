import json


INITIAL_CONFIG_DATA = {
    "default_drive_account": "",
    "default_frequency": "",
    "default_time": "",
    "backups": [],
}


def create_config_file():
    try:
        with open("config.json", "x") as config_file:
            json.dump(INITIAL_CONFIG_DATA, config_file, indent=4)
            return True

    except FileExistsError:
        return False
