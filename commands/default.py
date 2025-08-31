from utils.config_setup import load_config, save_config_to_file
from utils.validators import validate_configs


def default_handler(args: dict) -> None:
    if not args:
        print("No new defaults found. Nothing updated.")
        return

    try:
        total_configs = load_config()
    except ValueError as error:
        print(error)
        return

    if not (default_configs := validate_configs(args)):
        print("All given defaults are invalid. Nothing was updated.")
        return

    # Update keys to match defaults in config file (begin with default_)
    for config in list(default_configs):
        default_configs[f"default_{config}"] = default_configs.pop(config)

    total_configs.update(default_configs)

    save_config_to_file(total_configs)

    for config, value in default_configs.items():
        print(f"{config.replace('_', ' ').capitalize()} updated to {value}.")
