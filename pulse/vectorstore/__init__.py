"""Defines public vectorstores"""
import logging
import sys

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.vectorstore import VectorStore
from langchain.vectorstores.redis import Redis

from pulse import config

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("pulse.vectorstore")

def get_vectorstore() -> VectorStore:
    if config.vectorstore == "redis":

        redis = Redis(
            redis_url=config.redis_url + "/1",
            index_name="slack-messages",
            embedding=OpenAIEmbeddings(api_key=config.openai_api_key),
        )
        logger.debug("created redis vectorstore index: %s", redis.index_name)
        return redis
