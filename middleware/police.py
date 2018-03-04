from aiohttp import web
from aiohttp.web_exceptions import HTTPException, HTTPClientError
from middleware.errors import error


PLAIN_TYPE = "text/plain"
JSON_TYPE = "application/json"


@web.middleware
async def police_middleware(request, handler):
    try:
        response = await handler(request)
    except HTTPException as e:
        return e
    except HTTPClientError as e:
        return e
    except Exception as ex:
        return error()

    return response

