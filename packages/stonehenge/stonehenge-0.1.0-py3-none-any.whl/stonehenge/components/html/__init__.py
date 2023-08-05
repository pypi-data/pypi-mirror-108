from typing import Tuple, Union

from stonehenge.components.component import Component
from stonehenge.components.html.styles import HTMLStyle, render_style


class HTMLComponent(Component):
    style: HTMLStyle
    self_closing = False
    tag = ""

    def __init__(
        self,
        *children: Union[Component, Tuple[Component, ...]],
        content=None,
        style: Union[HTMLStyle, None] = None,
    ):
        self.children = children
        self.content = content
        self._style = style
        super().__init__(*children)

    def render(self):
        attrs = self.render_attrs() or ""
        content = self.content if self.content else ""
        raw_style = self._style or getattr(self, "style", None)
        style = render_style(raw_style) if raw_style else ""
        child_content = self.render_children()
        return f"<{self.tag} {attrs} {style}>{content}{child_content}</{self.tag}>"

    def render_attrs(self):
        pairs = [f"{k}={v}" for k, v in self.attrs.items()]
        return " ".join(pairs)

    @property
    def attrs(self):
        return {}


class HTML(HTMLComponent):
    tag = "html"

    def __init__(self, *args, charset="UTF-8", lang="en", **kwargs):
        self.charset = charset
        self.lang = lang
        super().__init__(*args, **kwargs)

    def render(self):
        return f"""<!DOCTYPE html>
<html lang="{self.lang}">
    <meta charset="{self.charset}">
    {self.render_children()}
</html>
"""


class Body(HTMLComponent):
    style = {"margin": 0}
    tag = "body"


class Div(HTMLComponent):
    tag = "div"


class H1(HTMLComponent):
    tag = "h1"


class P(HTMLComponent):
    tag = "p"


class A(HTMLComponent):
    tag = "a"

    def __init__(
        self,
        *args,
        href: Union[str, None] = None,
        target: Union[None, str] = None,
        **kwargs,
    ):
        self.href = href
        self.target = target
        super().__init__(*args, **kwargs)

    @property
    def attrs(self):
        attrs = {}
        if self.href:
            attrs["href"] = self.href
        if self.target:
            attrs["target"] = self.target
        return attrs
