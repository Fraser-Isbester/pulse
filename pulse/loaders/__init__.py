from pulse.loaders.slack import event_loader as slack_event_loader
from redis import Redis
from rq import Queue

redis = Redis(host="redis", port=6379, db=0)
job_queue = Queue(connection=redis)

__all__ = [
    "slack_event_loader",
]
