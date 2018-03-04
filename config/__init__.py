import yaml


def setup_config(app, root_path):
    with open(root_path / "config/config.yaml", 'r') as stream:
        try:
            app['config'] = yaml.load(stream)
            app['config']['root_path'] = root_path
        except yaml.YAMLError as exc:
            print(exc)
