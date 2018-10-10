import json
import traceback
from asyncio import CancelledError
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
        except IOError as e:
            request.app.loggers['rotating'].error(str(traceback.format_exc()))
            return e
        except CancelledError as e:
            request.app.loggers['rotating'].error(str(traceback.format_exc()))
            return e
        except KeyError as e:
            request.app.loggers['rotating'].error(str(traceback.format_exc()))
            return e
        except HTTPException as e:
            request.app.loggers['rotating'].error(str(traceback.format_exc()))
            return e
        except CustomHTTPException as e:
            pass
        except FileNotFoundError as e:
            request.app.loggers['rotating'].error(str(traceback.format_exc()))
            return CustomHTTPException(irc['NOT_FOUND'], 404)
        except Exception as e:
            request.app.loggers['rotating'].error(str(traceback.format_exc()))
            return CustomHTTPException()

        return response
    return errors_middleware_handler
