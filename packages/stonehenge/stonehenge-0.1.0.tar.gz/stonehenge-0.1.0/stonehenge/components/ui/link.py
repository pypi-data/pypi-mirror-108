from typing import Literal, Union
from stonehenge.components.component import Component
from stonehenge.components.ui.base import UIComponent
from stonehenge.components.html import A


class Link(UIComponent):
    def __init__(
        self,
        to: str,
        label: Union[str, None] = None,
        component: Union[None, Component] = None,
        target: Union[None, Literal["_blank"]] = None,
    ):
        self.to = to
        self.label = label
        self.component = component
        self.target = target

    def render(self):
        return A(
            href=self.to,
            target=self.target,
            content=self.label,
            style={
                "padding": "16px",
                "text_decoration": "none",
            },
        ).render()
