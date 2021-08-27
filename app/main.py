import uvicorn
from fastapi import FastAPI
from app.core.db.database import database
from app.core.db.redis import get_redis
from app.routers import redirect, api


app = FastAPI()

app.include_router(redirect.router)
app.include_router(api.router, prefix="/app/api/v1")


@app.on_event("startup")
async def startup():
    await database.connect()
    app.state.redis = await get_redis()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await app.state.redis.close()


@app.get('/')
async def health_check():
    return {"msg": "Hello, World"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
