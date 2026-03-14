from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.schemas.common import Ticker


class Settings(BaseSettings):
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    database_url: str = Field(
        default="postgresql+psycopg://crypto_user:crypto_password@db:5432/crypto_prices",
        alias="DATABASE_URL",
    )
    celery_broker_url: str = Field(
        default="redis://redis:6379/0",
        alias="CELERY_BROKER_URL",
    )
    celery_result_backend: str = Field(
        default="redis://redis:6379/1",
        alias="CELERY_RESULT_BACKEND",
    )
    deribit_base_url: str = Field(
        default="https://www.deribit.com/api/v2",
        alias="DERIBIT_BASE_URL",
    )
    tracked_tickers: str = Field(default="btc_usd,eth_usd", alias="TRACKED_TICKERS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def tracked_ticker_list(self) -> list[str]:
        tickers = [ticker.strip().lower() for ticker in self.tracked_tickers.split(",") if ticker.strip()]
        invalid_tickers = sorted(set(tickers) - set(Ticker.values()))
        if invalid_tickers:
            raise ValueError(
                f"Unsupported tickers in TRACKED_TICKERS: {', '.join(invalid_tickers)}. "
                f"Allowed values: {', '.join(Ticker.values())}."
            )
        return tickers


@lru_cache
def get_settings() -> Settings:
    return Settings()
