import os


def apply_routes(app):

    static = str(app.config['root_path']) + "/public/static"
    app.router.add_static("/static",
                          path=str(static),
                          name="static")

    for file in [file for file in os.listdir(app.config['root_path'] + "/routes/")
             if file != '__pycache__' and file != '__init__.py']:
        p, m = file.rsplit('.', 1)
        module_in_file = __import__("routes." + str(p))
        files_module = getattr(module_in_file, p)
        init = getattr(files_module, 'init')
        if "init" in dir():
            init(app)
            del init


