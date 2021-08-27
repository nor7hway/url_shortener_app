import os
import pytest


os.environ['TESTING'] = 'Test'


from alembic import command
from alembic.config import Config
from app.core.db import database
from sqlalchemy_utils import create_database, drop_database


@pytest.fixture(scope="module")
def temp_db():
    create_database(database.SQLALCHEMY_DATABASE_URL)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

    try:
        yield database.SQLALCHEMY_DATABASE_URL
    finally:
        drop_database(database.SQLALCHEMY_DATABASE_URL)
