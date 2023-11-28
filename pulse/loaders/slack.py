"""Contains slack loaders used for loading data from slack into the vectorstore."""
from pulse.vectorstore import redis
import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("pulse.loaders.slack")


async def event_loader(event):
    """
    Load slack events into the vectorstore.
    """

    logger.debug("got event: %s", event)

    if event.type != "message":
        logger.info("Ignoring event of type %s", event.type)
        return

    text = event.text
    meta = {k: v for k, v in event.__dict__.items() if k != "text"}
    meta["source"] = "slack"

    logger.debug("Adding message to vectorstore: %s, {%s}", text, meta)

    id = await redis.aadd_texts(texts=[text], metadata=meta)
    logging.debug("Added message to vectorstore: %s", id)
    return id
