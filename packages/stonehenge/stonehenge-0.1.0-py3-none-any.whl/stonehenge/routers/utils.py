def normalize_path(path: str) -> str:
    """Return a path with a leading slash and no trailing slash"""
    if not path.endswith("/"):
        path = f"{path}/"
    if not path.startswith("/"):
        path = f"/{path}"
    return path
