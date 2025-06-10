from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

def create_qa_chain(vector_db):
    llm = Ollama(model="llama2")  # use your Ollama model here
    retriever = vector_db.as_retriever()
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
