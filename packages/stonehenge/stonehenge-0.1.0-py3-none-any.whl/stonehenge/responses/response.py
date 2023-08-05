import json
from typing import List, Union

from stonehenge.components.component import Component
from stonehenge.responses.content_types import HTTPContentType

VALID_CONTENT_TYPES = Union[dict, str, Component]


class Response:
    def __init__(self, content: VALID_CONTENT_TYPES, content_type: HTTPContentType):
        self.content = content
        self.content_type = content_type

    def get_messages(self):
        initial_message = {
            "type": "http.response.start",
            "status": 200,
            "headers": self.get_response_headers(),
        }
        response_message = {
            "type": "http.response.body",
            "body": self.get_message_body(),
        }
        return [initial_message, response_message]

    def get_message_body(self) -> bytes:
        raise NotImplementedError

    def get_response_headers(self) -> List[List[bytes]]:
        return [[b"content-type", self.content_type.value]]


class HTMLResponse(Response):
    def __init__(self, content: Union[str, Component]):
        super().__init__(content, content_type=HTTPContentType.HTML)

    def get_message_body(self) -> bytes:
        if isinstance(self.content, str):
            return bytes(self.content, "utf-8")
        elif isinstance(self.content, Component):
            return bytes(self.content.render(), "utf-8")
        else:
            raise NotImplementedError


class JSONResponse(Response):
    def __init__(self, content: dict):
        super().__init__(content, content_type=HTTPContentType.JSON)

    def get_message_body(self):
        json_content = json.dumps(self.content)
        return bytes(json_content, "utf-8")


class ComponentResponse(Response):
    def __init__(self, component: Component):
        self.content: Component = component
        super().__init__(component, content_type=HTTPContentType.HTML)

    def get_message_body(self) -> bytes:
        return bytes(self.content.render(), "utf-8")
