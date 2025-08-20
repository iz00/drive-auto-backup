from pathlib import Path


def validate_and_get_absolute_local_path(path: str) -> str:
    if path and Path(path).exists():
        return str(Path(path).expanduser().resolve())

    raise ValueError("Invalid local path.")
