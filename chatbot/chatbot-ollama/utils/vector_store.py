from langchain.schema import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_store(texts: list[str]):
    docs = [Document(page_content=text) for text in texts]
    embeddings = OllamaEmbeddings()  # Use Ollama embeddings
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store
