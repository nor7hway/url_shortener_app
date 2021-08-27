import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID


metadata = sqlalchemy.MetaData()


users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", UUID(as_uuid=False),
                      server_default=sqlalchemy.text("uuid_generate_v4()"),
                      primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(100), unique=True,
                      nullable=False),
    sqlalchemy.Column("first_name", sqlalchemy.String(50)),
    sqlalchemy.Column("last_name", sqlalchemy.String(50)),
    sqlalchemy.Column("hashed_password", sqlalchemy.String(150)),
    sqlalchemy.Column("creation_date", sqlalchemy.DateTime()),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean(), nullable=False,
                      server_default=sqlalchemy.sql.expression.true()),
    sqlalchemy.Column("is_superuser", sqlalchemy.Boolean(), nullable=False,
                      server_default=sqlalchemy.sql.expression.false()),
)
