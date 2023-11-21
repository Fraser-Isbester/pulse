"""Defines public vectorstores"""
from langchain.vectorstores.redis import Redis
from langchain.embeddings import OpenAIEmbeddings

redis = Redis(
    redis_url="redis://redis:6379/1",
    index_name="slack_messages",
    embedding=OpenAIEmbeddings()
)
