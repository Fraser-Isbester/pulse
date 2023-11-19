from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain import hub
from langchain.chains import RetrievalQA


def main():

    # Load data and create embeddings
    data = load_data()


    db = FAISS.from_documents(data, OpenAIEmbeddings())

    # query = "What is an Autonomous Agent?"
    # docs = db.similarity_search(query)
    # print(docs)

    # Generates a RAG Chain
    chain = load_chain("zephyr", db)

    # Example query (replace with your actual use case)
    query = "What is an Autonomous Agent?"
    response = chain(query)
    print(response)

# Load your text file
def load_data() -> str:
    loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    all_splits = text_splitter.split_documents(data)
    return all_splits


# Create embeddings with FAISS
def create_embeddings(data):
    dimension = 768  # Example dimension, adjust as needed
    num_vectors = len(data)  # Number of vectors is the number of lines in your file

    # Creating a matrix with random data (replace this with your actual data embeddings)
    db_vectors = np.random.random((num_vectors, dimension)).astype('float32')

    # Building the index
    index = faiss.IndexFlatL2(dimension)
    index.add(db_vectors)
    return index

# Load a locally downloaded AI model with Langchain
def load_chain(model_name, vectorstore):
    llm = Ollama(
        model=model_name,
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": hub.pull("rlm/rag-prompt-llama")},
    )
    return qa_chain


if __name__ == '__main__':
    main()