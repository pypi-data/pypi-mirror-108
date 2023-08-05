from __future__ import annotations
from typing import List, Union

from .route import Route


class Router:
    def __init__(
        self,
        routes: List[Union[Route, Router]],
        path: str = "",
    ):
        self.path = path
        self.routes = routes
