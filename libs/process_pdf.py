from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from libs.allDirectories import allDirectories 
import os
from dotenv import load_dotenv
load_dotenv()

def process_pdf(file_path: str, doc_id: int):
    """Process PDF and create vector store"""


    loader = PyPDFLoader(file_path)
    documents = loader.load()

    if not documents or not all(doc.page_content for doc in documents):
        raise ValueError("No valid text content found in the PDF")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_documents(documents)

    collection_name = f"doc_{doc_id}"  


    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(texts, embeddings, persist_directory=f'{allDirectories['VECTORSTORE_DIR']}', collection_name=collection_name)
    
    vector_store.persist()

    return collection_name