from langchain import hub
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema.vectorstore import VectorStore


def get_retriever(vectorstore: VectorStore, model_name: str = "gpt-4-1106-preview") -> RetrievalQA:
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
