from collections.abc import Sequence
from datetime import date
from decimal import Decimal

from app.repositories.price_repository import PriceRepository
from app.schemas.price import LatestPriceResponse, PriceRecordResponse


class PriceService:
    def __init__(self, repository: PriceRepository) -> None:
        self.repository = repository

    def save_prices(self, records: Sequence[tuple[str, Decimal | float, int]]) -> Sequence[PriceRecordResponse]:
        normalized_records = [
            (ticker, price if isinstance(price, Decimal) else Decimal(str(price)), timestamp_unix)
            for ticker, price, timestamp_unix in records
        ]
        saved_records = self.repository.add_many(normalized_records)
        return [PriceRecordResponse.model_validate(record) for record in saved_records]

    def get_prices(self, ticker: str) -> Sequence[PriceRecordResponse]:
        return [PriceRecordResponse.model_validate(item) for item in self.repository.list_by_ticker(ticker)]

    def get_latest_price(self, ticker: str) -> LatestPriceResponse | None:
        record = self.repository.get_latest(ticker)
        if record is None:
            return None
        return LatestPriceResponse(
            ticker=record.ticker,
            price=record.price,
            timestamp_unix=record.timestamp_unix,
        )

    def get_prices_by_date(self, ticker: str, target_date: date) -> Sequence[PriceRecordResponse]:
        return [PriceRecordResponse.model_validate(item) for item in self.repository.list_by_date(ticker, target_date)]
