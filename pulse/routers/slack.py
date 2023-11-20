"""This defines the Slack API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum
from slack_sdk import WebClient, errors

v1 = APIRouter()
client = WebClient(token=SLACK_BOT_TOKEN)

class EventTypes(Enum):
    URL_VERIFICATION = "url_verification"
    REACTION_ADDED = "reaction_added"
    APP_MENTION = "app_mention"


class ChallengeRequestResponseType(BaseModel):
    token: str
    challenge: Optional[str]
    type: str


class SlackEventType(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str


class SlackEventCallbackType(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str
    event: "SlackEventType"


@v1.post("/event")
async def event(request: SlackEventCallbackType):
    """Responds to a Slack event."""

    # If a challenege event, return the challenge
    print(request)
    if request.type == EventTypes.URL_VERIFICATION.value:
        return ChallengeRequestResponseType(challenge=request.challenge)

    slack_event = request.event
    if slack_event.type != EventTypes.REACTION_ADDED.value:
        if slack_event["reaction"] != "eyes":
            pass

    elif slack_event.type != EventTypes.APP_MENTION.value:
        return

    raise HTTPException(status_code=400, detail="Unsupported slack event type")
