from config.config import config


def setup_config(app):
    setattr(app, 'config', config)
