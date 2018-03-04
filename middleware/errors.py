from aiohttp import web
from aiohttp.web_exceptions import HTTPException, HTTPClientError


PLAIN_TYPE = "text/plain"
JSON_TYPE = "application/json"


def error(message="Error", status=519):
    return web.Response(text=message,
                        status=status,
                        content_type=PLAIN_TYPE)


async def errors_middleware(app, handler):

    show_error_details = True

    async def errors_middleware_handler(request):
        try:
            response = await handler(request)
        except HTTPException as e:
            return e
        except HTTPClientError as e:
            return e
        except Exception as ex:
            if show_error_details:
                # return error details to the client
                return error(message=str(ex))
            # hide error details
            return error()

        return response
    return errors_middleware_handler

