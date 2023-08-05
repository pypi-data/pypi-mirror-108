from __future__ import annotations
from typing import Tuple, Union


class Component:
    def __init__(self, *children: Union[Component, Tuple[Component, ...]]):
        self.children = children

    def render(self) -> str:
        if hasattr(self, "child"):
            return getattr(self, "child").render()
        elif hasattr(self, "children"):
            return "".join([c.render() for c in getattr(self, "children")])
        raise NotImplementedError

    def render_children(self) -> str:
        child_content = ""
        for c in self.children:
            if isinstance(c, Component):
                child_content += c.render()
            elif isinstance(c, tuple):
                child_content += "".join([sub_child.render() for sub_child in c])
        return child_content
