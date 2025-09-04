def get_backups_ids(backups: list[dict]) -> set[int]:
    """Get all integer IDs in a list of backups."""
    return {backup.get("id") for backup in backups if isinstance(backup.get("id"), int)}


def filter_existing_backup_ids(
    backups_ids: set[int], candidate_ids: list[int]
) -> set[int]:
    """Return only the candidate IDs that exist in the given list of backups IDs."""
    return {backup_id for backup_id in candidate_ids if backup_id in backups_ids}


def format_config_label(config: str) -> str:
    return config.replace("_", " ").title()
