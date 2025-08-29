def filter_existing_backup_ids(
    backups: list[dict], candidate_ids: list[int]
) -> set[int]:
    """Return only the IDs that exist in the given list of backups."""
    existing_ids: set[int] = {
        backup.get("id") for backup in backups if isinstance(backup.get("id"), int)
    }

    return {backup_id for backup_id in candidate_ids if backup_id in existing_ids}
