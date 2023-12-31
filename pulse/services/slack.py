"""Contains Slack Client & Types."""
import logging
import sys
from enum import Enum
from typing import Optional

from pulse import config
from pydantic import BaseModel, ConfigDict
from slack_sdk import WebClient

logging.basicConfig(level=config.log_level, stream=sys.stdout)
logger = logging.getLogger(__name__)


client = WebClient(token=config.slack_token)


class EventWrapperTypes(Enum):
    URL_VERIFICATION = "url_verification"
    EVENT_CALLBACK = "event_callback"


class EventTypes(Enum):
    """Actual Slack Event Types."""

    MESSAGE = "message"
    REACTION_ADDED = "reaction_added"
    APP_MENTION = "app_mention"


class SlackEventItemType(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str
    channel: str
    ts: str


class SlackEventType(BaseModel):
    """Slack Event."""

    model_config = ConfigDict(extra="allow")

    type: str
    item: Optional[SlackEventItemType] = None


class SlackEventCallbackType(BaseModel):
    """Slack Event Request Wrapper."""

    model_config = ConfigDict(extra="allow")

    type: str
    event: SlackEventType


def get_message_from_event(client, event: SlackEventType):
    """Given a SlackEvent on a message, return that message text."""

    client.conversations_join(channel=event.item.channel)

    history = client.conversations_history(channel=event.item.channel, latest=event.item.ts, limit=1, inclusive=True)

    content = history["messages"][0]["text"] if history.get("messages") else None
    return content


def post_message(client, channel: str, text: str, thread_ts: Optional[str] = None):
    """Posts a message to a Slack channel."""

    logging.debug("Posting message to channel %s: %s", channel, text)
    client.chat_postMessage(channel=channel, text=text, thread_ts=thread_ts)
