"""This defines the Confluence API routes."""

import logging
import sys

from fastapi import APIRouter

from pulse.llm import get_retriever
from pulse.loaders import confluence_ingestor

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("pulse.routers.slack")

v1 = APIRouter()

@v1.post("/ingest")
async def ingest():
    """Trigger to ingest all labelled pages from confluence"""
    confluence_ingestor.load_all_labelled_docs()