from stonehenge.routers.route import Route
from stonehenge.routers.router import Router
from stonehenge.handlers.contrib import welcome_handler


DefaultRouter = Router(
    routes=[
        Route(methods=["GET"], path="/", handler=welcome_handler),
    ]
)
