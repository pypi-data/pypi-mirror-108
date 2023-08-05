from stonehenge.requests.request import Request
from stonehenge.responses.response import Response, JSONResponse


async def welcome_handler(request: Request) -> Response:
    return JSONResponse({"content": "this is the default welcome handler"})
