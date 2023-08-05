from typing import Awaitable, Callable, List

from stonehenge.requests.request import Request
from stonehenge.responses.response import Response
from stonehenge.requests.methods import ALLOWED_METHODS


class Route:
    def __init__(
        self,
        handler: Callable[[Request], Awaitable[Response]],
        methods: List[ALLOWED_METHODS],
        path: str,
    ):
        self.handler = handler
        self.methods = methods
        self.path = path
