from celery import Celery
from celery.schedules import crontab

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "crypto_prices",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.timezone = "UTC"
celery_app.conf.imports = ("app.tasks.price_tasks",)
celery_app.conf.beat_schedule = {
    "collect-crypto-prices-every-minute": {
        "task": "app.tasks.price_tasks.collect_prices_task",
        "schedule": crontab(minute="*"),
    }
}
