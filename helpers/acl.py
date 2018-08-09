import functools
from helpers.irc import irc
from middleware.errors import CustomHTTPException


def acl(roles: list):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
            allowed = False
            if len(roles) == 0:
                return await func(*args)
            try:
                for role in roles:
                    if role in args[0].user['roles']:
                        allowed = True
                        break

                if not allowed:
                    return CustomHTTPException(irc['ACCESS_DENIED'], 401)
            except:
                return CustomHTTPException(irc['ACCESS_DENIED'], 401)
            return await func(*args)
        return wrapped
    return wrapper
