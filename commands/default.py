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

    # Empty default configs should be allowed, but validation doesn't allow them
    empty_configs = {
        config: "" for config, value in args.items() if value.strip() == ""
    }
    for key in empty_configs:
        args.pop(key, None)

    if not (default_configs := validate_configs(args)) and not empty_configs:
        print("All given defaults are invalid. Nothing was updated.")
        return

    default_configs.update(empty_configs)

    # Update keys to match defaults in config file (begin with default_)
    for config in list(default_configs):
        default_configs[f"default_{config}"] = default_configs.pop(config)

    total_configs.update(default_configs)

    save_config_to_file(total_configs)

    for config, value in default_configs.items():
        value = value if value else '""'
        print(f"{config.replace('_', ' ').capitalize()} updated to {value}.")
