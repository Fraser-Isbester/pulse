"""Defines public vectorstores"""
from langchain.vectorstores.redis import Redis
from langchain.embeddings import OpenAIEmbeddings
from pulse import config

redis = Redis(
    redis_url="redis://redis:6379/1",
    index_name="slack-messages",
    embedding=OpenAIEmbeddings(api_key=config.openai_api_key),
)
print("Index Created:", redis.index_name)

ids = redis.add_texts(
    texts=["Fraser is a software engineer at Virta Health."],
    metadata={"source": "fraser", "ts": "2023-11-27"},
)
print("Added ids:", ids)
