"""Contains confluence loaders for loading data from confluence into the vectorstore."""
import logging
import sys

from atlassian import Confluence
from lxml import etree
from pulse.services import confluence
from pulse.vectorstore import vectorstore

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("pulse.loaders.confluence")

def load_all_labelled_docs():
    """
    Load all documents from a confluence space with "pulse" label into the vector store
    """
    # rest call to confluence with the username and api key
    docs = confluence.client.get_all_pages_by_label(label="pulse",)
    for doc in docs:
        # unfortunately the search by label doesn't provide expand option
        full_doc = confluence.client.get_page_by_id(page_id=doc.get("id"), expand="body.view")
        doc_loader(full_doc)
        
    return docs

def doc_loader(doc):
    """
    Load confluence documents into the vectorstore.
    """
    # rest call to confluence with the username and api key
    text = _strip_html_tags(doc.get("body").get("view").get("value"))
    
    meta = {k: v for k, v in doc.items() if k != "body"}
    meta["source"] = "confluence"
    
    logger.debug("Adding document to vectorstore: %s, {%s}", text, meta)
    
    id = vectorstore.aadd_texts(texts=[text], metadata=meta)
    logging.debug("Added document to vectorstore: %s", id)
    return id

    
def _strip_html_tags(text):
    """Remove html tags from a string"""
    return etree.HTML(text).xpath("string()")

# # for testing
# if __name__ == "__main__":
#     get_all_labelled_docs()