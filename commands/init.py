import json


def create_config_file(args):
    config_data = {
        "default_drive_account": "",
        "default_frequency": "",
        "default_time": "",
        "backups": [],
    }

    try:
        with open("config.json", "x") as config_file:
            json.dump(config_data, config_file, indent=4)
            print("Created file config.json.")

    except FileExistsError:
        print("File config.json already exists.")
