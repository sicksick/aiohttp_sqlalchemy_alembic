from aiohttp import web
from aiohttp.web_exceptions import HTTPException, HTTPClientError, HTTPUnauthorized
from middleware.errors import error


PLAIN_TYPE = "text/plain"
JSON_TYPE = "application/json"


@web.middleware
async def police_middleware(request, handler):
    try:
        if request.rel_url.raw_parts[1] == "api":
            raise HTTPUnauthorized()
        response = await handler(request)
    except HTTPException as e:
        return e
    except HTTPClientError as e:
        return e
    except Exception as ex:
        return error()

    return response

