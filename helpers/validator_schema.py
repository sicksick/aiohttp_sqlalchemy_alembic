from aiohttp.http_exceptions import HttpProcessingError
from cerberus import Validator

from middleware.errors import CustomHTTPException


async def validate(data, schema):
    v = Validator()

    if v.validate(data, schema) is False:
        print(v.errors)
        raise CustomHTTPException(v.errors, 422)

    return True
