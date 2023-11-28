"""This defines the Slack API routes."""

from fastapi import APIRouter, HTTPException, Request
from pulse.llm import get_retriever
import logging
import sys

from pulse.loaders import slack_event_loader
from pulse.services.slack import (
    EventTypes,
    EventWrapperTypes,
    SlackEventCallbackType,
)
import pulse.services.slack as slack

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

v1 = APIRouter()


@v1.post("/event")
async def event(request: Request):
    """Responds to a Slack event."""

    request = await request.json()
    logging.debug("Received /event dir: %s", request)


    # If a challenege event, return the challenge
    if request["type"] == EventWrapperTypes.URL_VERIFICATION.value:
        return {"challenge": request.challenge}
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

    # TODO: push this to a processing queue
    await slack_event_loader(request.event)

    # Respond to an SOSd message
    # TODO: Move this to a processing queue
    # TODO: Migrate this into a service call abstraction

    # if slack_event.type == EventTypes.REACTION_ADDED.value:
    #     if slack_event.reaction == "eyes":
    #         await slack_query_responder(request)

    slack_event, item = request.event, request.event.item
    if slack_event.type == EventTypes.REACTION_ADDED.value:

        if slack_event.reaction == "sos":
            history = slack.get_message_from_event(
                slack.client,
                slack_event
            )
            chat_response = get_retriever()(history)
            slack.post_message(
                slack.client,
                channel=slack_event.item.channel,
                text=chat_response["result"]
            )

            # logger.debug("sos reaction recieved, processing response...")
            # join = client.conversations_join(channel=item.channel)

            # if not join["ok"]:
            #     raise HTTPException(status_code=400, detail=f"Slack API Error: {join}")

            # history = client.conversations_history(
            #     channel=item.channel, latest=item.ts, limit=1, inclusive=True
            # )

            # content = history["messages"][0]["text"] if history.get("messages") else None

            # if not content:
            #     raise HTTPException(status_code=400, detail="No message content")

            # retriever = get_retriever()
            # chat_response = retriever(content)

            # client.chat_postMessage(
            #     channel=item.channel,
            #     text=chat_response["result"],
            #     thread_ts=item.ts,
            # )

    return {"status": "accepted"}
