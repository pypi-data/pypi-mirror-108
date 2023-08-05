from typing import Literal, Union

GET_METHOD = Literal["GET"]
POST_METHOD = Literal["POST"]

ALLOWED_METHODS = Union[
    GET_METHOD,
    POST_METHOD,
]
