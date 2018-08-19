import os

import aiohttp_jinja2


def init(app):
    app.router.add_get('/app', front_app)
    app.router.add_get('/', home)


@aiohttp_jinja2.template('index.html')
async def home(request):
    GOOGLE_SIGNIN_CLIENT_ID = os.getenv('GOOGLE_SIGNIN_CLIENT_ID', None)
    facebook_id = os.getenv('FACEBOOK_ID', None)
    url_redirect_after_login = os.getenv('URL_REDIRECT_AFTER_LOGIN', None)
    return {
        'FACEBOOK_ID': facebook_id,
        'URL_REDIRECT_AFTER_LOGIN': url_redirect_after_login,
        'GOOGLE_SIGNIN_CLIENT_ID': GOOGLE_SIGNIN_CLIENT_ID
    }


@aiohttp_jinja2.template('app.html')
async def front_app(request):
    return {'data': ''}
