"""This defines the Slack API routes."""

import logging
import sys

from fastapi import APIRouter, HTTPException, Request

import pulse.services.slack as slack
from pulse.llm import get_retriever
from pulse.loaders import slack_event_loader
from pulse.services.slack import (EventTypes, EventWrapperTypes,
                                  SlackEventCallbackType)

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("pulse.routers.slack")

v1 = APIRouter()


@v1.post("/event")
async def event(request: Request):
    """Responds to a Slack event."""

    request = await request.json()
    logging.debug("Received /event dir: %s", request)

    # If a challenege event, return the challenge
    if request["type"] == EventWrapperTypes.URL_VERIFICATION.value:
        return {"challenge": request["challenge"]}

    # If not an event callback, return an error
    if typ := request["type"] != EventWrapperTypes.EVENT_CALLBACK.value:
        raise HTTPException(status_code=400, detail=f"Unknown event wrapper type '{typ}'")

    # Turn the request into a pydantic model
    try:
        request = SlackEventCallbackType.model_validate(request)
    except ValueError as e:
        logger.exception("Error validating request: %s", e)
        raise HTTPException(status_code=400, detail="Error validating request")
    logger.debug("Validated request: %s", request)

    ## Event Processing Below ##

    # TODO(fraser-isbester): push this to a processing queue
    # https://github.com/Fraser-Isbester/pulse/issues/4
    await slack_event_loader(request.event)

    chat_completion_retriever = get_retriever()
    match request.event:
        # TODO(fraser-isbester): push this to a processing queue
        # https://github.com/Fraser-Isbester/pulse/issues/4
        case event if event.type == EventTypes.REACTION_ADDED.value and event.reaction == "eyes":
            logger.debug("Received actionable event: %s", event)
            history = slack.get_message_from_event(slack.client, event)
            chat_response = chat_completion_retriever(history)
            slack.post_message(
                slack.client, channel=event.item.channel, text=chat_response["result"], thread_ts=event.item.ts
            )

    return {"status": "accepted"}
