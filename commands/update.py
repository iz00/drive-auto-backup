from collections.abc import Callable

from utils.backup_utils import filter_existing_backup_ids
from utils.config_setup import load_config, save_config_to_file
from utils.validators import CONFIGS_VALIDATORS


def update_handler(args: dict) -> None:
    try:
        total_configs = load_config()
    except ValueError as error:
        print(error)
        return

    updatable_ids = filter_existing_backup_ids(
        total_configs["backups"], args.pop("ids")
    )

    if not updatable_ids:
        print("No matching backup IDs found. Nothing was updated.")
        return

    if not args:
        print("No new configs found. Nothing was updated.")
        return

    if not (updated_configs := validate_updates(args)):
        print("All given configs are invalid. Nothing was updated.")
        return

    for backup in total_configs["backups"]:
        if backup.get("id") in updatable_ids:
            backup.update(updated_configs)

    save_config_to_file(total_configs)

    print("Updated backups with IDs:", *updatable_ids)


def validate_updates(args: dict) -> dict:
    """
    Validate a dict of config updates, returning only valid entries.
    Invalid values are reported and skipped.
    """
    valid_updates = {}

    for config, value in args.items():
        validator: Callable[[str], str] = CONFIGS_VALIDATORS[config]

        try:
            valid_updates[config] = validator(value)
        except ValueError as error:
            print(error)

    return valid_updates
