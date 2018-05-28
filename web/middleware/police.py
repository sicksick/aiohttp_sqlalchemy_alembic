import traceback

from aiohttp import web
from aiohttp.web_exceptions import HTTPException, HTTPUnauthorized
from middleware.errors import CustomHTTPException


@web.middleware
async def police_middleware(request, handler):
    try:
        if request.rel_url.raw_parts[1] == "api":
            raise HTTPUnauthorized()
        response = await handler(request)
    except HTTPException as e:
        return e
    except CustomHTTPException as e:
        return e
    except Exception as e:
        request.app.loggers['rotating'].error(str(traceback.format_exc()))
        return CustomHTTPException()

    return response

