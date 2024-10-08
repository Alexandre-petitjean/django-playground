import os

from celery import Celery
from kombu import Exchange
from kombu import Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("django_playground")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configuration des exchanges et des queues
app.conf.task_queues = (
    # Queue normale pour Celery
    Queue(
        "celery",
        Exchange("celery", type="direct"),
        routing_key="celery",
        queue_arguments={
            "x-dead-letter-exchange": "dead_letter_exchange",  # DLX exchange
            "x-dead-letter-routing-key": "dead_letter_routing_key",  # DLX routing key
        },
    ),
    # Dead Letter Queue (pour les messages échoués)
    Queue(
        "dead_letter_queue",
        Exchange("dead_letter_exchange", type="direct"),
        routing_key="dead_letter_routing_key",
    ),
)

# Optionnel : configuration des routes si vous voulez spécifier quelle tâche va dans quelle queue
# app.conf.task_routes = {
#     'myapp.tasks.my_task': {'queue': 'celery'},  # Exemple de route pour une tâche
# }
