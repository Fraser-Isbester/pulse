import logging
import sys
from enum import Enum

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.vectorstore import VectorStore

from pulse import config

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("pulse.vectorstore")

class VectorStoreTypes(Enum):
    """Supported VectorStores"""
    REDIS = "redis"
    PGVECTOR = "pgvector"


def get_vectorstore(config, vectorstore: VectorStoreTypes = VectorStoreTypes.REDIS) -> VectorStore:

    # TODO(fraser-isbester): make these configurable
    # https://github.com/Fraser-Isbester/pulse/issues/3
    index_name = "slack-messages"
    embedding = OpenAIEmbeddings(api_key=config.openai_api_key)

    match vectorstore:
        case VectorStoreTypes.REDIS:
            # Note: Lazy import for mutually exclusive dependencies
            from langchain.vectorstores.redis import Redis
            return Redis(
                redis_url=config.redis_url + "/1",
                index_name=index_name,
                embedding=embedding,
            )
        case VectorStoreTypes.PGVECTOR:
            # Note: Lazy import for mutually exclusive dependencies
            from langchain.vectorstores.redis import PGVector
            return PGVector(
                postgres_url=config.postgres_url,
                index_name=index_name,
                embedding=embedding,
            )

    raise ValueError(f"unknown vectorstore: {vectorstore}")


# TODO(fraser-isbester): Parameterize call
# https://github.com/Fraser-Isbester/pulse/issues/3
vectorstore = get_vectorstore(config, vectorstore=VectorStoreTypes.REDIS)
