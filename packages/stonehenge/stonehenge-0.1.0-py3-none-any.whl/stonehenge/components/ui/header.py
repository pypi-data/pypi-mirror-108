from typing import List, Literal, Union
from stonehenge.components.component import Component
from stonehenge.components.ui import Box
from stonehenge.exceptions import InvalidInvocationException

HeaderLayout = Union[
    Literal["left-right"],
]
LinkListType = List[Component]


class Header(Component):
    def __init__(
        self,
        left: LinkListType = [],
        right: LinkListType = [],
        layout: HeaderLayout = "left-right",
    ):
        self.left = left
        self.right = right
        self.layout = layout

    def render(self) -> str:
        if self.layout == "left-right":
            if not self.left or not self.right:
                msg = "Left-Right header layout missing components to render"
                raise InvalidInvocationException(msg)
            return Box(
                Box(*self.left),
                Box(*self.right),
                style={
                    "display": "flex",
                    "justify_content": "space-between",
                    "padding": "8px",
                },
            ).render()
        else:
            raise NotImplementedError
