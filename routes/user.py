import uuid

import aiohttp

import bcrypt
import jwt
from aiohttp import web
from aiohttp.web import json_response

from helpers.acl import acl
from helpers.irc import irc
from middleware.errors import CustomHTTPException
from model import Role, User


def init(app):
    prefix = '/api/user'
    app.router.add_post(prefix + '/login', login)
    app.router.add_post(prefix + '', create_user)
    app.router.add_post(prefix + '/login/facebook', user_facebook_login)


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


async def user_facebook_login(request):
    data = await request.post()
    status = data.get('status', None)
    token = data.get('token', None)
    if status == 'connected':

        facebook_url_me = f'https://graph.facebook.com/me?redirect=false&access_token={token}'
        async with aiohttp.ClientSession() as session:
            async with session.get(facebook_url_me) as r:
                data_from_facebook = await r.json()
                user = await User.get_user_by_facebook_id(data_from_facebook['id'])
                if not user:
                    data_user = dict()
                    # TODO создать пользователя
                    password = str(uuid.uuid4()).encode('utf-8')
                    data_user['password'] = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
                    data_user['roles'] = ['user']
                    data_user['facebook_id'] = data_from_facebook['id']
                    if 'name' in data_from_facebook:
                        name_list = data_from_facebook['name'].split(' ')
                        if len(name_list) > 1:
                            data_user['firstname'] = ' '.join(name_list[:-1])
                            data_user['lastname'] = name_list[-1]
                        else:
                            data_user['firstname'] = data_from_facebook['name']
                    user_id = await User.create_user(data_user)

                    user = await User.get_user_by_id(user_id)
                    roles = [role['name'] for role in await Role.get_roles_by_id(user['id']) if role['name']]

                    if bcrypt.checkpw(password, str(user['password']).encode('utf-8')):
                        del user['password']
                        encoded = jwt.encode({'user': user, 'roles': roles}, request.app.config['secret'],
                                             algorithm='HS256').decode('utf-8')
                    else:
                        return CustomHTTPException(irc['ACCESS_DENIED'], 401)

                    return json_response({'token': encoded, 'user': user, 'roles': roles})
                else:
                    roles = [role['name'] for role in await Role.get_roles_by_id(user['id']) if role['name']]
                    del user['password']
                    encoded = jwt.encode({'user': user, 'roles': roles}, request.app.config['secret'],
                                         algorithm='HS256').decode('utf-8')
                    return json_response({'token': encoded, 'user': user, 'roles': roles})

    return json_response({"status": "failed"}, status=401)


async def login(request):
    data = await request.json()
    users = await User.get_user_by_email(data['email'])
    if len(users) == 1:
        password = users[0]['password'].encode('utf-8')
        if bcrypt.checkpw(str(data['password']).encode('utf-8'), password):
            roles = [role['name'] for role in await Role.get_roles_by_id(users[0]['id']) if role['name']]
            encoded = jwt.encode({'user': users[0], "roles": roles}, request.app.config['secret'],
                                 algorithm='HS256').decode('utf-8')
        else:
            return CustomHTTPException(irc['ACCESS_DENIED'], 401)
    else:
        return CustomHTTPException(irc['USER_NOT_FOUND'], 404)
    return json_response({"token": encoded, "roles": roles})
