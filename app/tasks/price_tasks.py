from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from decimal import Decimal

import aiohttp
from celery import shared_task

from app.clients.deribit import DeribitClient
from app.core.config import get_settings
from app.db.session import get_session_factory
from app.repositories.price_repository import PriceRepository
from app.services.price_service import PriceService


def collect_prices() -> None:
    prices = asyncio.run(_fetch_prices())
    session_factory = get_session_factory()

    with session_factory() as session:
        service = PriceService(PriceRepository(session))
        timestamp_unix = int(datetime.now(tz=timezone.utc).timestamp())
        service.save_prices(
            [(ticker, price, timestamp_unix) for ticker, price in prices.items()]
        )


async def _fetch_prices() -> dict[str, Decimal]:
    settings = get_settings()
    client = DeribitClient(settings.deribit_base_url)
    tickers = settings.tracked_ticker_list

    async with aiohttp.ClientSession() as session:
        values = await asyncio.gather(*(client.get_index_price(ticker, session) for ticker in tickers))

    return dict(zip(tickers, values, strict=True))


@shared_task(name="app.tasks.price_tasks.collect_prices_task")
def collect_prices_task() -> None:
    collect_prices()
