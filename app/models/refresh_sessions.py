import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID


metadata = sqlalchemy.MetaData()


refresh_sessions_table = sqlalchemy.Table(
    "refresh_sessions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True,
                      unique=True, autoincrement=True),
    sqlalchemy.Column("user_id", UUID(as_uuid=False), nullable=False),
    sqlalchemy.Column("token", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("user_agent", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("expiration_date", sqlalchemy.DateTime(),
                      nullable=False),
    sqlalchemy.Column("creation_date", sqlalchemy.DateTime(), nullable=False),
)
