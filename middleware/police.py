import traceback

import jwt
from aiohttp import web
from aiohttp.web_exceptions import HTTPException
from model import User, Role
from middleware.errors import CustomHTTPException
from helpers.irc import irc


@web.middleware
async def police_middleware(request, handler):
    try:
        if 'api/user/login' in str(request.rel_url):
            response = await handler(request)
            return response
        if request.rel_url.raw_parts[1] == "api":
            data = request.headers.get('Authorization')
            if not data:
                return CustomHTTPException(irc['ACCESS_DENIED'], 401)
            try:
                decode = jwt.decode(data[6:], request.app.config['secret'], algorithms=['HS256'])
                user = await User.get_user_by_id(decode['user']['id'])
                user['roles'] = [role['name'] for role in await Role.get_roles_by_id(user['id']) if role['name']]
                if decode['user']['email'] == user['email']:
                    request.user = user
                    response = await handler(request)
                    return response
            except Exception as e:
                print(str(e))
                return CustomHTTPException(irc['ACCESS_DENIED'], 401)
        response = await handler(request)
    except HTTPException as e:
        return e
    except CustomHTTPException as e:
        return e
    except Exception as e:
        request.app.loggers['rotating'].error(str(traceback.format_exc()))
        return CustomHTTPException()

    return response

