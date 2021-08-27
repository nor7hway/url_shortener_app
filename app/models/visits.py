import sqlalchemy


from app.models.urls import urls_table


metadata = sqlalchemy.MetaData()


visits_table = sqlalchemy.Table(
    "visits",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True,
                      unique=True, autoincrement=True),
    sqlalchemy.Column("device", sqlalchemy.String(75)),
    sqlalchemy.Column("country", sqlalchemy.String(50)),
    sqlalchemy.Column("visit_date", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("url_id", sqlalchemy.ForeignKey(urls_table.c.id,
                                                      ondelete='CASCADE',
                                                      onupdate='CASCADE')),
)
