from os import environ
import databases


DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")
DB_HOST = environ.get("DB_HOST")
DB_NAME = environ.get("DB_NAME")

TESTING = environ.get("TESTING")

if TESTING:
    DB_NAME = "testdb"

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)
