from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app.core.config import settings
from app.core.database import Base

from app.models.user import User
from app.models.user_preference import UserPreference
from app.models.procedure import Procedure
from app.models.query_history import QueryHistory
from app.models.document import Document
from app.models.document_verification import DocumentVerification
from app.models.guidance_history import GuidanceHistory
from app.models.feedback import Feedback
from app.models.government_source import GovernmentSource
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use the database URL from .env
database_url = settings.database_url.replace(
    "postgresql+asyncpg://",
    "postgresql+psycopg://",
)

config.set_main_option(
    "sqlalchemy.url",
    database_url.replace("%", "%%"),
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()