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


class VectorStoreFactory:
    def __init__(self, config):
        self.config = config
        self._vectorstore = None
        self._vectorstore_type = None

    def get_vectorstore(self, vectorstore_type: VectorStoreTypes = VectorStoreTypes.REDIS) -> VectorStore:
        """Returns a vectorstore instance."""

        if self._vectorstore_type and vectorstore_type != self._vectorstore_type:
            raise ValueError(f"vectorstore already created with type: {self._vectorstore_type}")

        if not self._vectorstore:
            self._vectorstore = self._create_vectorstore(vectorstore_type)
            self._vectorstore_type = vectorstore_type

        return self._vectorstore

    def _create_vectorstore(self, vectorstore_type: VectorStoreTypes = VectorStoreTypes.REDIS) -> VectorStore:

        # TODO(fraser-isbester): make these configurable
        # https://github.com/Fraser-Isbester/pulse/issues/3
        index_name = "pulse"
        embedding = OpenAIEmbeddings(api_key=config.openai_api_key)

        match vectorstore_type:
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

        raise ValueError(f"unknown vectorstore: {vectorstore_type}")

vectorstorefactory = VectorStoreFactory(config)

def get_vectorstore(vectorstore_type: VectorStoreTypes = VectorStoreTypes.PGVECTOR):
    """This is a convenience function for FastAPIs dependency system."""
    return vectorstorefactory.get_vectorstore(vectorstore_type)
