import argparse

from commands.add import add_handler
from commands.init import init_handler
from commands.remove import remove_handler
from commands.update import update_handler
from commands.default import default_handler
from commands.list import list_handler


parser = argparse.ArgumentParser(
    description="Automate backups to Google Drive",
    epilog="Also check and update backups in config.json",
)

main_commands_subparser = parser.add_subparsers(
    title="commands", description="Main actions commands", required=True
)


# INIT COMMAND
init_command_parser = main_commands_subparser.add_parser(
    "init",
    help="Create a blank config.json file",
    epilog="File is only created if it doesn't already exist",
)
init_command_parser.set_defaults(func=init_handler)


# ADD COMMAND
add_command_parser = main_commands_subparser.add_parser(
    "add",
    help="Add a new backup to config.json",
    epilog="Also check and update backups in config.json. Schedule backups after adding them",
)
add_command_parser.add_argument(
    "--local", help="Local path to backup", metavar="PATH", dest="local_path"
)
add_command_parser.add_argument(
    "--drive",
    help="Drive folder to backup to (ID available in URL)",
    metavar="DRIVE_FOLDER_ID",
    dest="drive_folder",
)
add_command_parser.add_argument(
    "--account",
    help="Google Drive account email",
    metavar="EMAIL",
    dest="drive_account",
)
add_command_parser.add_argument(
    "--freq",
    help="Backup frequency (e.g. 15m, 2h, 1d, 1w)",
    metavar="FREQUENCY",
    dest="frequency",
)
add_command_parser.add_argument("--time", help="Time backup is done", metavar="HH:MM")
add_command_parser.set_defaults(func=add_handler)


# REMOVE COMMAND
remove_command_parser = main_commands_subparser.add_parser(
    "remove",
    aliases=["rm"],
    help="Remove backups from config.json (and unschedule it)",
)
remove_command_parser.add_argument(
    "ids", nargs="+", type=int, help="IDs of backups in config.json"
)
remove_command_parser.set_defaults(func=remove_handler)


# UPDATE COMMAND
update_command_parser = main_commands_subparser.add_parser(
    "update",
    help="Update a backup in config.json",
    argument_default=argparse.SUPPRESS,
)
update_command_parser.add_argument(
    "ids", nargs="+", help="IDs of backups in config.json", type=int
)
update_command_parser.add_argument(
    "--local", help="Local path to backup", metavar="PATH", dest="local_path"
)
update_command_parser.add_argument(
    "--drive",
    help="Drive folder to backup to (ID available in URL)",
    metavar="DRIVE_FOLDER_ID",
    dest="drive_folder",
)
update_command_parser.add_argument(
    "--account",
    help="Google Drive account email",
    metavar="EMAIL",
    dest="drive_account",
)
update_command_parser.add_argument(
    "--freq",
    help="Backup frequency (e.g. 15m, 2h, 1d, 1w)",
    metavar="FREQUENCY",
    dest="frequency",
)
update_command_parser.add_argument(
    "--time", help="Time backup is done", metavar="HH:MM"
)
update_command_parser.set_defaults(func=update_handler)


# LIST COMMAND
list_command_parser = main_commands_subparser.add_parser(
    "list",
    aliases=["ls"],
    help="List backups in config.json",
)
list_command_parser.add_argument(
    "ids", nargs="*", help="IDs of backups in config.json", type=int
)
list_command_parser.add_argument(
    "-d", "--defaults", action="store_true", help="Show default values in config.json"
)
list_command_parser.add_argument(
    "-v", "--verbose", action="store_true", help="Show more info about each backup"
)
list_command_parser.set_defaults(func=list_handler)


# DEFAULT COMMAND
default_command_parser = main_commands_subparser.add_parser(
    "default",
    help="Set default values for backups",
    argument_default=argparse.SUPPRESS,
)
default_command_parser.add_argument(
    "--account",
    help="Default Google Drive account email",
    metavar="EMAIL",
    dest="drive_account",
)
default_command_parser.add_argument(
    "--freq",
    help="Default frequency for backups (e.g. 15m, 2h, 1d, 1w)",
    metavar="FREQUENCY",
    dest="frequency",
)
default_command_parser.add_argument(
    "--time", help="Default time for backups", metavar="HH:MM"
)
default_command_parser.set_defaults(func=default_handler)


# RUN COMMAND
run_command_parser = main_commands_subparser.add_parser(
    "run", help="Manually run backups now"
)
run_command_parser.add_argument(
    "ids", nargs="*", help="IDs of backups in config.json", type=int
)
run_command_parser.add_argument(
    "--all", action="store_true", help="Run all backups now"
)


# SCHEDULE COMMAND
schedule_command_parser = main_commands_subparser.add_parser(
    "schedule",
    help="Schedule backups from config.json",
)
schedule_command_parser.add_argument(
    "ids", nargs="*", help="IDs of backups in config.json", type=int
)
schedule_command_parser.add_argument(
    "--all", action="store_true", help="Schedule all backups"
)


# UNSCHEDULE COMMAND
unschedule_command_parser = main_commands_subparser.add_parser(
    "unschedule",
    help="Unschedule backups from tasks",
)
unschedule_command_parser.add_argument(
    "ids", nargs="*", help="IDs of backups in config.json", type=int
)
unschedule_command_parser.add_argument(
    "--all", action="store_true", help="Unschedule all backups"
)


# AUTHENTICATE COMMAND
authenticate_command_parser = main_commands_subparser.add_parser(
    "authenticate",
    aliases=["auth"],
    help="Authenticate Google Drive accounts emails",
)
authenticate_command_parser.add_argument(
    "accounts", nargs="*", help="Google Drive accounts emails"
)
all_or_unauthenticated_group = (
    authenticate_command_parser.add_mutually_exclusive_group()
)
all_or_unauthenticated_group.add_argument(
    "--all", action="store_true", help="All Google Drive accounts in config.json"
)
all_or_unauthenticated_group.add_argument(
    "--unauthenticated",
    action="store_true",
    help="All yet unauthenticated Google Drive accounts in config.json",
)


arguments = parser.parse_args()

command_arguments = vars(arguments).copy()
del command_arguments["func"]

arguments.func(command_arguments)
