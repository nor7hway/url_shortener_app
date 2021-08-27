from datetime import datetime


from app.core.db.database import database
from app.models.visits import visits_table


async def create_visit(url_id: int, device: str, country: str):
    query = (
        visits_table.insert()
        .values(
            device=device,
            country=country,
            visit_date=datetime.now(),
            url_id=url_id,
        )
        .returning(
            visits_table.c.id
        )
    )
    return await database.fetch_one(query)
