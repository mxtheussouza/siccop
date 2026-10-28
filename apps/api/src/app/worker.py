import dramatiq
from dramatiq.brokers.redis import RedisBroker

from app.core.config import Settings
from app.core.logging import configure_logging

settings = Settings()
configure_logging(settings.log_level)
broker = RedisBroker(url=settings.redis_url.get_secret_value())
dramatiq.set_broker(broker)
# Actors are added in Phase 06. No placeholder tasks pretend to process uploads.
