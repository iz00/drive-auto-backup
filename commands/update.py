from utils.backup_utils import *
from utils.config_setup import load_config, save_config_to_file
from utils.validators import validate_configs


def update_handler(args: dict) -> None:
    try:
        total_configs = load_config()
    except ValueError as error:
        print(error)
        return

    updatable_ids = filter_existing_backup_ids(
        get_backups_ids(total_configs["backups"]), args.pop("ids")
    )

    if not updatable_ids:
        print("No matching backup IDs found. Nothing was updated.")
        return

    if not args:
        print("No new configs found. Nothing was updated.")
        return

    if not (updated_configs := validate_configs(args)):
        print("All given configs are invalid. Nothing was updated.")
        return

    for backup in total_configs["backups"]:
        if backup.get("id") in updatable_ids:
            backup.update(updated_configs)

    save_config_to_file(total_configs)

    print("Updated backups with IDs:", *updatable_ids)
