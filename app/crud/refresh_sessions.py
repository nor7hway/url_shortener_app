from datetime import datetime, timedelta


from app.core.db.database import database
from app.models.refresh_sessions import refresh_sessions_table


async def create_session(user_id: int, user_agent: str, token: str):
    query = (
        refresh_sessions_table.insert()
        .values(
            user_id=user_id,
            token=token,
            user_agent=user_agent,
            expiration_date=datetime.now() + timedelta(weeks=12),
            creation_date=datetime.now()
        )
        .returning(
            refresh_sessions_table.c.id
        )
    )
    return await database.fetch_one(query)


async def delete_session(token: str):
    query = (
        refresh_sessions_table.delete()
        .where(
            refresh_sessions_table.c.token == token
        )
    )
    return await database.execute(query)


async def get_session(refresh_token: str):
    query = (
        refresh_sessions_table.select()
        .where(
            refresh_sessions_table.c.token == refresh_token
        )
    )
    return await database.fetch_one(query)
