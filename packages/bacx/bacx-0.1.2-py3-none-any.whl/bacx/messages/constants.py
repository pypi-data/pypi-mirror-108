import os
from enum import Enum


class MessageBrokers(Enum):
    NONE = "none"
    REDIS = "redis"
    GOOGLE_PUBSUB = "google_pub_sub"


MESSAGE_BROKER = MessageBrokers(os.environ.get("MESSAGE_BROKER") or "none")
REDIS_URL = os.environ.get("REDIS_URL", "redis")
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")
PUBSUB_TOPIC_TEMPLATE = os.environ.get("PUBSUB_TOPIC_TEMPLATE", "message-pub-{type}-dev")
PUBSUB_SUBSCRIPTION_TEMPLATE = os.environ.get("PUBSUB_SUBSCRIPTION_TEMPLATE", "message-sub-{type}-dev")
REDIS_QUEUE_TEMPLATE = os.environ.get("REDIS_QUEUE_TEMPLATE", "message-queue-{type}")
