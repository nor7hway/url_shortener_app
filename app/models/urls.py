import sqlalchemy


from app.models.users import users_table


metadata = sqlalchemy.MetaData()


urls_table = sqlalchemy.Table(
    "urls",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, autoincrement=True,
                      nullable=False, primary_key=True),
    sqlalchemy.Column("hash", sqlalchemy.String(16), index=True),
    sqlalchemy.Column("original_url", sqlalchemy.String(512), nullable=False),
    sqlalchemy.Column("creation_date", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("expiration_date", sqlalchemy.DateTime(),
                      nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id,
                                                       ondelete='CASCADE',
                                                       onupdate='CASCADE')),
)
