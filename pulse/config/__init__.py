"""Handy place for configuration variables."""
from os import environ

from dotenv import load_dotenv

load_dotenv()

log_level = environ.get("LOG_LEVEL", "DEBUG")

vectorstore = environ.get("VECTORSTORE", "redis")
redis_url = environ.get("REDIS_URL", "redis://redis:6379")
postgres_url = environ.get("POSTGRES_URL", "postgresql+pg8000://postgres@postgres:5432")

slack_token = environ.get("SLACK_BOT_TOKEN")
openai_api_key = environ.get("OPENAI_API_KEY")
confluence_username = environ.get("CONFLUENCE_USERNAME")
confluence_api_key = environ.get("CONFLUENCE_API_KEY")
confluence_space = environ.get("CONFLUENCE_SPACE")
confluence_url = environ.get("CONFLUENCE_URL")
