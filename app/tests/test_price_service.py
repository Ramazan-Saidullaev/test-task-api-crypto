from app.repositories.price_repository import PriceRepository
from app.services.price_service import PriceService


def test_service_returns_latest_price(db_session):
    service = PriceService(PriceRepository(db_session))
    service.save_prices(
        [
            ("btc_usd", 40000.0, 1700000000),
            ("btc_usd", 41000.0, 1700000060),
        ]
    )

    latest = service.get_latest_price("btc_usd")

    assert latest is not None
    assert float(latest.price) == 41000.0
    assert latest.timestamp_unix == 1700000060
