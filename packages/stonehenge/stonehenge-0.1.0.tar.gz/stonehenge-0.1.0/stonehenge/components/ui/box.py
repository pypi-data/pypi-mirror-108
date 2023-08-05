from stonehenge.components.html.styles import HTMLStyle
from typing import Literal, Union
from stonehenge.components.ui.base import UIComponent
from stonehenge.components.html import Div

DisplayProperty = Union[
    Literal["flex"],
    Literal["block"],
    Literal["inline-block"],
]


class Box(UIComponent):
    def __init__(self, *children, style: HTMLStyle = {}):
        self.children = children
        self.style = style

    def render(self) -> str:
        return Div(
            *self.children,
            style=self.style,
        ).render()
