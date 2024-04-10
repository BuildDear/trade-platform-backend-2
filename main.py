from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core import Base
from core.models.db_helper import db_helper
from api_v1.traders.views import router as traders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(traders_router)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
