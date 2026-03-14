import pytest


@pytest.mark.anyio
async def test_get_latest_price_returns_404_when_ticker_not_found(client):
    response = await client.get("/prices/latest", params={"ticker": "btc_usd"})

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_prices_returns_saved_records(client, price_service):
    price_service.save_prices(
        [
            ("btc_usd", 42000.5, 1700000000),
            ("btc_usd", 42100.5, 1700000060),
        ]
    )

    response = await client.get("/prices", params={"ticker": "btc_usd"})

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.anyio
async def test_get_latest_price_returns_last_saved_record(client, price_service):
    price_service.save_prices(
        [
            ("btc_usd", 42000.5, 1700000000),
            ("btc_usd", 42100.5, 1700000060),
        ]
    )

    response = await client.get("/prices/latest", params={"ticker": "btc_usd"})

    assert response.status_code == 200
    assert response.json()["timestamp_unix"] == 1700000060


@pytest.mark.anyio
async def test_get_prices_by_date_filters_records(client, price_service):
    price_service.save_prices(
        [
            ("eth_usd", 2000.0, 1700000000),
            ("eth_usd", 2100.0, 1700086400),
        ]
    )

    response = await client.get(
        "/prices/by-date",
        params={
            "ticker": "eth_usd",
            "date": "2023-11-14",
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.anyio
async def test_missing_ticker_returns_422(client):
    response = await client.get("/prices")

    assert response.status_code == 422


@pytest.mark.anyio
async def test_invalid_ticker_returns_422(client):
    response = await client.get("/prices", params={"ticker": "sol_usd"})

    assert response.status_code == 422
