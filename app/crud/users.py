from datetime import datetime

from sqlalchemy.sql.expression import update

from app.schemas import users as users_scheme
from app.models.users import users_table
from app.core.db.database import database


async def create_user(user: users_scheme.CreateUser, hashed_password: str):
    query = (
        users_table.insert()
        .values(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=hashed_password,
            creation_date=datetime.now(),
        )
        .returning(
            users_table.c.email,
            users_table.c.first_name,
            users_table.c.last_name,
        )
    )
    return await database.fetch_one(query)


async def change_user_password(user_id, hashed_password):
    query = (
        update(users_table)
        .where(users_table.c.id == user_id)
        .values(hashed_password=hashed_password)
    )
    return await database.execute(query)


async def get_user_by_email(email: str):
    query = users_table.select().where(users_table.c.email == email)
    return await database.fetch_one(query)


async def get_user_by_id(user_id: int):
    query = users_table.select().where(users_table.c.id == user_id)
    return await database.fetch_one(query)
