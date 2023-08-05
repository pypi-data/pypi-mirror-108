from typing import Dict, Union, TypedDict

SpacingUnit = Union[int, str]
SpacingProperty = Union[
    SpacingUnit, Dict[str, SpacingUnit]  # For responsive breakpoints
]


class HTMLStyle(TypedDict, total=False):
    align_content: str
    align_items: str
    background_color: str
    color: str
    display: str
    justify_content: str
    max_width: Union[int, str]
    margin: SpacingProperty
    padding: SpacingProperty
    width: str


def render_style(style: HTMLStyle) -> str:
    rules = []
    for k, v in style.items():
        attr = k.replace("_", "-")
        if isinstance(k, str):
            value = v
        else:
            raise NotImplementedError
        rules.append(f"{attr}: {value}; ")
    rendered = "".join(rules)
    return f'style="{rendered}"'
