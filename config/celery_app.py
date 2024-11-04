import os

from celery import Celery
from kombu import Exchange
from kombu import Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("django_playground")

# Using a string here means the worker doesn't have to serialize.
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configuration des exchanges et des queues
app_key = "stock"

############################################
# Configuration des exchanges et queue DLX
############################################
dlx_stock_exchange = Exchange(f"dlx_{app_key}", type="direct")

dlx_stock_queues = [
    Queue(f"q.dlx.{app_key}", dlx_stock_exchange, routing_key=app_key),
    Queue(f"q.dlx.{app_key}.timeout", dlx_stock_exchange, routing_key="timeout"),
]

stock_dlx_args = {
    "x-dead-letter-exchange": f"dlx_{app_key}",  # DLX exchange
    "x-dead-letter-routing-key": app_key,  # DLX routing key
    "x-message-ttl": 10000,  # TTL
}

############################################
# Configuration des exchanges business
############################################
stock_exchange = Exchange(app_key, type="topic")

app.conf.task_queues = (
    Queue(f"q.{app_key}.order", stock_exchange, routing_key="stock.order", queue_arguments=stock_dlx_args),
    Queue(f"q.{app_key}.send", stock_exchange, routing_key="stock.send", queue_arguments=stock_dlx_args),
    *dlx_stock_queues,
)
