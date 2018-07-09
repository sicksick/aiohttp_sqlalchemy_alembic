import aiohttp_jinja2
import jinja2


def jinja_init(app):
    path = app.config['root_path'] + "/public/templates"
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(path))
