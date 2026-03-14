from collections.abc import Sequence
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

from sqlalchemy import Select, desc, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.price import PriceRecord


class PriceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_many(self, records: Sequence[tuple[str, Decimal, int]]) -> list[PriceRecord]:
        items = [
            PriceRecord(ticker=ticker.lower(), price=price, timestamp_unix=timestamp_unix)
            for ticker, price, timestamp_unix in records
        ]
        try:
            self.session.add_all(items)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

        for item in items:
            self.session.refresh(item)
        return items

    def list_by_ticker(self, ticker: str) -> Sequence[PriceRecord]:
        stmt = self._base_ticker_query(ticker).order_by(PriceRecord.timestamp_unix.asc())
        return self.session.scalars(stmt).all()

    def get_latest(self, ticker: str) -> PriceRecord | None:
        stmt = self._base_ticker_query(ticker).order_by(desc(PriceRecord.timestamp_unix)).limit(1)
        return self.session.scalars(stmt).first()

    def list_by_date(self, ticker: str, target_date: date) -> Sequence[PriceRecord]:
        day_start = datetime.combine(target_date, time.min, tzinfo=timezone.utc)
        next_day = day_start + timedelta(days=1)
        stmt = (
            self._base_ticker_query(ticker)
            .where(PriceRecord.timestamp_unix >= self._to_unix(day_start))
            .where(PriceRecord.timestamp_unix < self._to_unix(next_day))
            .order_by(PriceRecord.timestamp_unix.asc())
        )
        return self.session.scalars(stmt).all()

    def _base_ticker_query(self, ticker: str) -> Select[tuple[PriceRecord]]:
        return select(PriceRecord).where(PriceRecord.ticker == ticker.lower())

    @staticmethod
    def _to_unix(value: datetime) -> int:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return int(value.timestamp())
