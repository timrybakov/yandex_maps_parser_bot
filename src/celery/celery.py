from celery import Celery

from ..di import di_container

app = Celery(
    'yandex_maps_parser_bot',
    broker=di_container.settings.redis_url,
    backend=di_container.settings.redis_url
)
