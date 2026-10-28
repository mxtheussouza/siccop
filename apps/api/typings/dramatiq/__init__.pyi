# Narrow typing surface for Dramatiq 1.18, which does not ship PEP 561 types.
from dramatiq.brokers.redis import RedisBroker

def set_broker(broker: RedisBroker) -> None: ...
