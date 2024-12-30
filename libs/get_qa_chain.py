from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from libs.allDirectories import allDirectories 
from dotenv import load_dotenv
load_dotenv()

def get_qa_chain(vector_store_path: str):
    """Create QA chain from vector store with context"""
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(collection_name=vector_store_path, persist_directory=f'{allDirectories['VECTORSTORE_DIR']}', embedding_function=embeddings)
    
    llm = ChatOpenAI(temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True
    )
    
    return qa_chain