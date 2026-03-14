from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_price_service
from app.schemas.common import Ticker
from app.schemas.price import LatestPriceResponse, PriceRecordResponse
from app.services.price_service import PriceService

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("", response_model=list[PriceRecordResponse])
def get_prices(
    ticker: Ticker = Query(..., description="Ticker to search, for example btc_usd"),
    service: PriceService = Depends(get_price_service),
):
    return service.get_prices(ticker)


@router.get("/latest", response_model=LatestPriceResponse)
def get_latest_price(
    ticker: Ticker = Query(..., description="Ticker to search, for example btc_usd"),
    service: PriceService = Depends(get_price_service),
):
    result = service.get_latest_price(ticker)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No prices found for ticker '{ticker.value}'",
        )
    return result


@router.get("/by-date", response_model=list[PriceRecordResponse])
def get_prices_by_date(
    ticker: Ticker = Query(..., description="Ticker to search, for example btc_usd"),
    date: date = Query(..., description="Date in YYYY-MM-DD format"),
    service: PriceService = Depends(get_price_service),
):
    return service.get_prices_by_date(ticker=ticker, target_date=date)
