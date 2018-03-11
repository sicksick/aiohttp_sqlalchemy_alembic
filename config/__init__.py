import yaml


def setup_config(app, root_path):
    with open(root_path / "config/config.yaml", 'r') as stream:
        try:
            config = yaml.load(stream)
            config['root_path'] = str(root_path)
            setattr(app, 'config', config)
        except yaml.YAMLError as exc:
            print(exc)
