"""Handy place for configuration variables."""
from os import environ
from dotenv import load_dotenv

load_dotenv()

redis_url = environ.get("REDIS_URL", "redis://redis:6379")
slack_token = environ["SLACK_BOT_TOKEN"]
openai_api_key = environ["OPENAI_API_KEY"]
