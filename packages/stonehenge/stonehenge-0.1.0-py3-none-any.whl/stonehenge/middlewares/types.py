from typing import Callable

from ..requests.request import Request

Middleware = Callable[[Request], Request]
