from typing import List, Union

from stonehenge.admin.handlers import admin_home
from stonehenge.routers.route import Route
from stonehenge.routers.router import Router


class AdminRouter(Router):

    routes: List[Union[Route, Router]] = [
        Route(
            methods=["GET"],
            path="/",
            handler=admin_home,
        )
    ]

    def __init__(self, path: str = "/admin"):
        return super().__init__(routes=self.routes, path=path)
