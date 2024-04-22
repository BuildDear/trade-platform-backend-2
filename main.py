from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1.traders.views import router as traders_router
from api_v1.auth.views import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(traders_router)
app.include_router(auth_router)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
