from utils.backup_utils import filter_existing_backup_ids
from utils.config_setup import load_config, save_config_to_file


def remove_handler(args: dict) -> None:
    try:
        total_configs = load_config()
    except OSError:
        print("Error: config.json not found.")
        return

    try:
        backups: list[dict] = total_configs["backups"]
    except KeyError:
        print('Error: config.json is malformed (missing "backups" array).')
        return

    removable_ids = filter_existing_backup_ids(backups, args["ids"])

    if not removable_ids:
        print("No matching backup IDs found. Nothing was removed.")
        return

    total_configs["backups"] = [
        backup for backup in backups if backup.get("id") not in removable_ids
    ]

    save_config_to_file(total_configs)

    print("Removed backups with IDs:", *removable_ids)
