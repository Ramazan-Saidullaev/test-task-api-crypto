from __future__ import annotations

from decimal import Decimal
from typing import Any

import aiohttp


class DeribitClientError(Exception):
    pass


class DeribitClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def get_index_price(self, ticker: str, session: aiohttp.ClientSession) -> Decimal:
        url = f"{self.base_url}/public/get_index_price"
        params = {"index_name": ticker.lower()}

        try:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                payload = await response.json()
        except aiohttp.ClientError as exc:
            raise DeribitClientError(f"Failed to fetch index price for ticker '{ticker}'") from exc

        self._raise_on_api_error(payload, ticker)
        result = payload.get("result")
        if not result or "index_price" not in result:
            raise DeribitClientError(f"Unexpected Deribit response for ticker '{ticker}'")

        return Decimal(str(result["index_price"]))

    @staticmethod
    def _raise_on_api_error(payload: dict[str, Any], ticker: str) -> None:
        error = payload.get("error")
        if error:
            message = error.get("message", "Unknown Deribit error")
            raise DeribitClientError(f"Deribit returned an error for ticker '{ticker}': {message}")
