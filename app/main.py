from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # noqa: F401
from app.api.routes.prices import router as prices_router
from app.db.session import Base, ensure_database_schema, get_engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_database_schema()
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(
    title="Crypto Price API",
    description="API for Deribit crypto index prices",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(prices_router)


@app.get("/")
def read_root():
    return {"message": "Crypto Price API is running"}
