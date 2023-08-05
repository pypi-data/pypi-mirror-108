from stonehenge.requests.request import Request
from stonehenge.responses.response import JSONResponse


async def cms_home(request: Request):
    return JSONResponse({"foo": "bar"})
