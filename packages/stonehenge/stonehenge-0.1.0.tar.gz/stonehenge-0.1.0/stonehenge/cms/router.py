from typing import List, Union

from stonehenge.cms.handlers import cms_home
from stonehenge.routers.route import Route
from stonehenge.routers.router import Router


class CMSRouter(Router):

    routes: List[Union[Route, Router]] = [
        Route(
            methods=["GET"],
            path="/",
            handler=cms_home,
        )
    ]

    def __init__(self, path: str = "/cms"):
        return super().__init__(routes=self.routes, path=path)
