"""This defines the Slack API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum
from slack_sdk import WebClient
from pulse import config, chat
import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

v1 = APIRouter()
client = WebClient(token=config.slack_token)


class EventTypes(Enum):
    URL_VERIFICATION = "url_verification"
    REACTION_ADDED = "reaction_added"
    APP_MENTION = "app_mention"


class ChallengeRequestResponseType(BaseModel):
    token: str
    challenge: Optional[str]
    type: str


class SlackEventItemType(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str
    channel: str
    ts: str


class SlackEventType(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str
    item: Optional[SlackEventItemType]


class SlackEventCallbackType(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str
    event: "SlackEventType"


@v1.post("/event")
async def event(request: SlackEventCallbackType):
    """Responds to a Slack event."""
    logging.debug("Received /event: %s", request)

    # If a challenege event, return the challenge
    if request.type == EventTypes.URL_VERIFICATION.value:
        return ChallengeRequestResponseType(challenge=request.challenge)

    slack_event, item = request.event, request.event.item
    if slack_event.type == EventTypes.REACTION_ADDED.value:
        if slack_event.reaction != "eyes":
            raise HTTPException(
                status_code=400,
                detail="Unsupported slack event type (reaction != eyes))",
            )

        join = client.conversations_join(channel=item.channel)
        logging.debug("joined: %s", join)
        if not join["ok"]:
            raise HTTPException(status_code=400, detail=f"Slack API Error: {join}")

        history = client.conversations_history(
            channel=item.channel, latest=item.ts, limit=1, inclusive=True
        )

        content = history["messages"][0]["text"] if history.get("messages") else None
        if not content:
            raise HTTPException(status_code=400, detail="No message content")

        chat_response = chat()(content)
        response = client.chat_postMessage(
            channel=item.channel,
            text=chat_response["result"],
            thread_ts=item.ts,
        )
        print("response:", response)
        return {"status": "accepted"}

    raise HTTPException(status_code=400, detail="Unsupported slack event type")
