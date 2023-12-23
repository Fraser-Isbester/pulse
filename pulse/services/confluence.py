"""Contains Confluence Client & Types."""
import logging
import sys

from atlassian import Confluence
from pulse import config

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("pulse.services.confluence")

class ConfluenceFactory:
    def __init__(self, config):
        self.config = config
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = Confluence(
                url=config.confluence_url,
                username=config.confluence_username,
                password=config.confluence_api_key,
                cloud=True,
            )
        return self._client

confluencefactory = ConfluenceFactory(config)
