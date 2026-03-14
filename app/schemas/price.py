from datetime import date as date_type
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import Ticker


class PriceRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticker: Ticker
    price: Decimal
    timestamp_unix: int


class LatestPriceResponse(BaseModel):
    ticker: Ticker
    price: Decimal
    timestamp_unix: int


class PriceByDateQuery(BaseModel):
    ticker: Ticker = Field(..., description="Ticker name, for example btc_usd")
    date: date_type = Field(..., description="Date in YYYY-MM-DD format")
