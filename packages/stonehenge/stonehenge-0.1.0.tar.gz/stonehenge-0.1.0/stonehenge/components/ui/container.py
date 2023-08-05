from stonehenge.components.html import Div
from stonehenge.components.ui.base import UIComponent
from stonehenge.components.ui.constants import CONTAINER_WIDTH


class Container(UIComponent):
    def render(self):
        return Div(
            Div(
                *self.children,
                style={
                    "max_width": CONTAINER_WIDTH,
                    "width": "100%",
                    "background_color": "blue",
                }
            ),
            style={
                "background_color": "orange",
                "display": "flex",
                "justify_content": "center",
                "padding": "16px",
                "width": "100%",
            },
        ).render()
