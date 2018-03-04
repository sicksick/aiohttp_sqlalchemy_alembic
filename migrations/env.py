from __future__ import with_statement
import os, sys
sys.path.append(os.getcwd())
from sqlalchemy import engine_from_config, pool, MetaData, Table
import yaml
from alembic import context
from logging.config import fileConfig
config = context.config
fileConfig(config.config_file_name)
model_list = dir()
from model import *
new_model = [model for model in dir() if model not in model_list]


def combine_metadata(*args):
    m = MetaData()
    for metadata in args:
        for t in metadata.tables.values():
            t.tometadata(m)
    return m


module_in_file = __import__("model")
meta_list = list()

for item in new_model:
    try:
        files_module = getattr(module_in_file, item)
        if isinstance(files_module, Table) is True:
            meta_list.append(files_module.metadata)
    except:
        continue


target_metadata = combine_metadata(permission.metadata, permission_user.metadata, user.metadata)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = str()
    with open("config/config.yaml", 'r') as stream:
        try:
            config = yaml.load(stream)
            connection = config['connection']
            url = f"{connection['type']}://{connection['user']}:{connection['password']}@" \
                  f"{connection['host']}:{connection['port']}/{connection['database']}"
        except yaml.YAMLError as exc:
            print(exc)


    # url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = str()
    with open("config/config.yaml", 'r') as stream:
        try:
            config_yaml = yaml.load(stream)
            connection = config_yaml['connection']
            url = f"{connection['type']}://{connection['user']}:{connection['password']}@" \
                  f"{connection['host']}:{connection['port']}/{connection['database']}"
        except yaml.YAMLError as exc:
            print(exc)

    config_dict = config.get_section(config.config_ini_section)
    config_dict['sqlalchemy.url'] = url

    connectable = engine_from_config(
        config_dict,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
