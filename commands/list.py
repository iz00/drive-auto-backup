from tabulate import tabulate

from utils.backup_utils import *
from utils.config_setup import get_default_configs, load_config


def list_handler(args: dict) -> None:
    try:
        total_configs = load_config()
    except ValueError as error:
        print(error)
        return

    if args.get("defaults"):
        print(f"\n{format_defaults(get_default_configs(total_configs))}\n")

        if not args.get("ids"):
            return

    if not args.get("ids"):
        listable_ids = get_backups_ids(total_configs["backups"])
    else:
        listable_ids = filter_existing_backup_ids(
            get_backups_ids(total_configs["backups"]), args.get("ids")
        )

    if not listable_ids:
        print("No matching backup IDs found. Nothing was updated.")
        return

    backups_to_list = [
        backup
        for backup in total_configs["backups"]
        if backup.get("id") in listable_ids
    ]

    print(f"\n{format_backups(backups_to_list, args.get('verbose'))}\n")


def format_defaults(defaults: dict) -> str:
    formatted_defaults = ["Default configs:"]

    for config, value in defaults.items():
        config = format_config_label(config)
        value = value if value else "(not set)"

        formatted_defaults.append(f"\t{config}: {value}")

    return "\n".join(formatted_defaults)


def format_backups(backups: list[dict], verbose: bool) -> str:
    if not verbose:

        for i, backup in enumerate(backups):
            backups[i] = {
                format_config_label(config): value
                for config, value in backup.items()
                if config not in ("frequency", "time", "last_backup")
            }

        return tabulate(backups, headers="keys", tablefmt="simple")

    formatted_backups: list[str] = []

    for backup in backups:
        formatted_backup = "\n".join(
            f"{format_config_label(config)}: {value}"
            for config, value in backup.items()
        )
        formatted_backups.append(formatted_backup)

    return f"\n{'-'*30}\n".join(formatted_backups)
