import logging
import sys
from enum import Enum

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.vectorstore import VectorStore

from pulse import config

logging.basicConfig(level=config.log_level, stream=sys.stdout)
logger = logging.getLogger(__name__)

class VectorStoreTypes(Enum):
    """Supported VectorStores"""
    REDIS = "redis"
    PGVECTOR = "pgvector"


def get_vectorstore(config, vectorstore: VectorStoreTypes = VectorStoreTypes.REDIS) -> VectorStore:

    # TODO(fraser-isbester): make these configurable
    # https://github.com/Fraser-Isbester/pulse/issues/3
    index_name = "pulse"
    embedding = OpenAIEmbeddings(api_key=config.openai_api_key)

    match vectorstore:
        case VectorStoreTypes.REDIS:
            # Note: Lazy import for mutually exclusive dependencies
            from langchain.vectorstores.redis import Redis
            return Redis(
                redis_url=config.redis_url + "/1", # NOTE: Redis DB 1 (0 reserved for rq)
                index_name=index_name,
                embedding=embedding,
            )
        case VectorStoreTypes.PGVECTOR:
            # Note: Lazy import for mutually exclusive dependencies
            from langchain.vectorstores.pgvector import PGVector
            return PGVector(
                connection_string=config.postgres_url,
                collection_name=index_name,
                embedding_function=embedding,
            )

    raise ValueError(f"unknown vectorstore: {vectorstore}")


# TODO(fraser-isbester): Parameterize call
# https://github.com/Fraser-Isbester/pulse/issues/3
vectorstore = get_vectorstore(config, vectorstore=VectorStoreTypes.PGVECTOR)
