import re

from typing import List, Pattern

from .utils import normalize_path

REGEX_MAP = {
    "int": "(\\d+)",
    "slug": "[-\\w]+",
    "str": "(\\w+)",
}

part_regex = re.compile(":(\\w+)<(\\w+)>")


def path_to_regex(path: str) -> Pattern[str]:
    parts: List[str] = []
    for part in path.split("/"):
        if match := part_regex.match(part):
            param, param_type = match.groups()
            pattern_part = f"(?P<{param}>{REGEX_MAP[param_type]})"
            parts.append(pattern_part)

        else:
            parts.append(part)
    pattern = normalize_path("/".join(parts))
    return re.compile(pattern)
