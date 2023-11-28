
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# from langchain.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain import hub
from langchain.chains import RetrievalQA

from pulse.vectorstore import redis

def get_retriever(model_name: str="gpt-4-1106-preview", vectorstore=redis) -> RetrievalQA:
    """Builds the RAG Chain."""

    llm = ChatOpenAI(
        model=model_name,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": hub.pull("rlm/rag-prompt-llama")},
    )

    return qa_chain
