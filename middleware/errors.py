import json
import traceback
from aiohttp.web_exceptions import HTTPException
from aiohttp.web_response import Response
from helpers.irc import irc


class CustomHTTPException(Response, Exception):

    def __init__(self, body=irc['INTERNAL_SERVER_ERROR'], status=500):
        Response.__init__(self,
                          status=status,
                          headers=None,
                          reason=None,
                          text=None,
                          content_type='application/json',
                          body=json.dumps({"errors": body}),
        )


async def errors_middleware(app, handler):

    async def errors_middleware_handler(request):
        try:
            response = await handler(request)
        except HTTPException as e:
            return e
        except CustomHTTPException as e:
            return e
        except Exception as e:
            request.app.loggers['rotating'].error(str(traceback.format_exc()))
            return CustomHTTPException()

        return response
    return errors_middleware_handler

