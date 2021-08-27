from datetime import datetime, timedelta
from sqlalchemy import and_, select, join
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.functions import count


from app.core.db.database import database
from app.models.urls import urls_table
from app.models.users import users_table
from app.models.visits import visits_table
from app.schemas import urls as url_scheme


async def get_urls_by_user_id(user_id: str):
    query = (
        select(
            [
                urls_table.c.hash,
                urls_table.c.original_url,
                urls_table.c.creation_date,
                urls_table.c.expiration_date,
                count(visits_table.c.id).label("visits_count")
            ]
        )
        .select_from(
            join(
                join(users_table, urls_table, users_table.c.id == urls_table.c.user_id),
                visits_table,
                urls_table.c.id == visits_table.c.url_id
            )
        )
        .where(
            users_table.c.id == user_id
        )
        .group_by(
            urls_table.c.hash,
            urls_table.c.original_url,
            urls_table.c.creation_date,
            urls_table.c.expiration_date,
        )
        .order_by(
            desc(urls_table.c.creation_date)
        )
    )
    return await database.fetch_all(query)


async def get_url_by_hash(hash: str):

    query = urls_table.select().where(urls_table.c.hash == hash)
    return await database.fetch_one(query)


async def create_url(url: url_scheme.CreateUrl, hash_url: str,
                     user_id: str = None):
    query = (
        urls_table.insert()
        .values(
            hash=hash_url,
            original_url=url.original_url,
            creation_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(weeks=1),
            user_id=user_id,
        )
        .returning(
            urls_table.c.hash,
            urls_table.c.original_url,
            urls_table.c.creation_date,
            urls_table.c.expiration_date,
        )
    )
    return await database.fetch_one(query)


async def delete_url(hash: str, user_id: str):
    query = (
        urls_table.delete()
        .where(
            and_(
                urls_table.c.hash == hash,
                users_table.c.id == user_id
            )
        )
        .where()
    )
    return await database.execute(query)
