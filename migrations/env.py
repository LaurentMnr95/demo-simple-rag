import logging
from logging.config import fileConfig
import os

from alembic import context
from sqlalchemy import engine_from_config
from dotenv import dotenv_values


from app.extensions.database.models import BaseSQLAlchemyModel

logger = logging.getLogger(__name__)

env_config = dotenv_values(
    os.getcwd() + "/.env"
)  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
config.set_main_option(  # type:ignore
    "sqlalchemy.url", env_config["SQLALCHEMY_DATABASE_URI_ADMIN"]  # type:ignore
)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = BaseSQLAlchemyModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    def process_revision_directives(context, revision, directives):  # type:ignore
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]  # type:ignore
            if script.upgrade_ops.is_empty():  # type:ignore
                directives[:] = []
                logger.info("No changes in schema detected.")

    a = config.get_section(config.config_ini_section)
    assert a is not None
    engine = engine_from_config(a, prefix="sqlalchemy.")
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,  # type:ignore
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
