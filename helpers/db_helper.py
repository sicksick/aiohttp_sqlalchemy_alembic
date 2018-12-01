import datetime
from helpers.irc import irc
from middleware.errors import CustomHTTPException


def as_dict(obj):
    if isinstance(obj, list):
        for items in obj:
            for item in items:
                if isinstance(items[item], datetime.datetime):
                    items[item] = str(items[item])
                if isinstance(items[item], datetime.timedelta):
                    items[item] = str(items[item])
        return obj
    if isinstance(obj, dict):
        for item in obj:
            if isinstance(obj[item], datetime.datetime):
                obj[item] = str(obj[item])
            if isinstance(obj[item], datetime.timedelta):
                obj[item] = str(obj[item])
        return obj
    return obj


async def raise_db_exception(e):
    error = irc['INTERNAL_SERVER_ERROR']
    if len(e.args) > 0:
        error = {
            "ERROR_MESSAGE": e.args[0],
            "ERROR_CODE": None
        }
    raise CustomHTTPException(error, 422)
