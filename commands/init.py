from utils.config_setup import create_config_file


def init_handler(args):
    if create_config_file():
        print("Created file config.json.")
    else:
        print("File config.json already exists.")
