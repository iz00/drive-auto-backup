from utils.backup_utils import *
from utils.config_setup import load_config, save_config_to_file


def remove_handler(args: dict) -> None:
    try:
        total_configs = load_config()
    except ValueError as error:
        print(error)
        return

    removable_ids = filter_existing_backup_ids(
        get_backups_ids(total_configs["backups"]), args["ids"]
    )

    if not removable_ids:
        print("No matching backup IDs found. Nothing was removed.")
        return

    total_configs["backups"] = [
        backup
        for backup in total_configs["backups"]
        if backup.get("id") not in removable_ids
    ]

    save_config_to_file(total_configs)

    print("Removed backups with IDs:", *removable_ids)
