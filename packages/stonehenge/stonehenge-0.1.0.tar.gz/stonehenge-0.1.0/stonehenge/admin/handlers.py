from stonehenge.requests.request import Request
from stonehenge.responses.response import HTMLResponse
from stonehenge.components.html import HTML, Body, Div, H1, P
from stonehenge.components.ui import Container


async def admin_home(request: Request) -> HTMLResponse:
    component = HTML(
        Body(
            Container(P(content="I am in a container")),
            Div(
                H1(content="Hello world!", style={"color": "blue"}),
                P(content="This is a p tag!", style={"color": "orange"}),
                P(content="And so is this one!"),
            ),
        )
    )
    return HTMLResponse(component)
