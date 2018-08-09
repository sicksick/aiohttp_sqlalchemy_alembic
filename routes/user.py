import bcrypt
import jwt
from aiohttp.web import json_response

from helpers.acl import acl
from helpers.irc import irc
from middleware.errors import CustomHTTPException
from model import Role, User


def init(app):
    prefix = '/api/user'
    app.router.add_post(prefix + '/login', login)
    app.router.add_post(prefix + '', create_user)


@acl(['admin'])
async def create_user(request):
    data = await request.json()

    if 'password' not in data or 'email' not in data or 'roles' not in data:
        return CustomHTTPException(irc['EMAIL_ROLES_AND_PASSWORD_IS_REQUIRED'], 422)

    users = await User.get_user_by_email(data['email'])
    if len(users) >= 1:
        return CustomHTTPException(irc['USER_EXISTS'], 404)

    password = data['password'].encode('utf-8')
    data['password'] = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    user_id = await User.create_user(data)

    user = await User.get_user_by_id(user_id)
    roles = [role['name'] for role in await Role.get_roles_by_id(user['id']) if role['name']]

    if bcrypt.checkpw(password, str(user['password']).encode('utf-8')):
        encoded = jwt.encode({'user': user, 'roles': roles}, request.app.config['secret'], algorithm='HS256').decode('utf-8')
    else:
        return CustomHTTPException(irc['ACCESS_DENIED'], 401)

    return json_response({"roles": roles})


async def login(request):
    data = await request.json()
    users = await User.get_user_by_email(data['email'])
    if len(users) == 1:
        password = users[0]['password'].encode('utf-8')
        if bcrypt.checkpw(str(data['password']).encode('utf-8'), password):
            roles = [role['name'] for role in await Role.get_roles_by_id(users[0]['id']) if role['name']]
            encoded = jwt.encode({'user': users[0], "roles": roles}, request.app.config['secret'], algorithm='HS256').decode('utf-8')
        else:
            return CustomHTTPException(irc['ACCESS_DENIED'], 401)
    else:
        return CustomHTTPException(irc['USER_NOT_FOUND'], 404)
    return json_response({"token": encoded, "roles": roles})
