"""Defines public vectorstores"""
from langchain.vectorstores.redis import Redis
from langchain.embeddings import OpenAIEmbeddings
from pulse import config
import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("pulse.vectorstore")

redis = Redis(
    redis_url=config.redis_url + "/1",
    index_name="slack-messages",
    embedding=OpenAIEmbeddings(api_key=config.openai_api_key),
)
logger.debug("created redis vectorstore index: %s", redis.index_name)
