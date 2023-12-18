"""Contains Confluence Client & Types."""
import logging
import sys

from atlassian import Confluence
from pulse import config

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("pulse.services.confluence")

client = Confluence(
    url=config.confluence_url,
    username=config.confluence_username,
    password=config.confluence_api_key,
    cloud=True,
)

