from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.fake import FakeEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, AzureBlobStorageFileLoader
import re
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# PyPDFDirectoryLoader
import os 
import logging 


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
# Load and split the PDF document.


def format_filename(filename: str) -> str:
    return re.sub(r'\s+', '_', filename)

def load_dir(path):
    logging.log(f"Loading documents from directory: {path}")
    loader = DirectoryLoader(path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    logging.log(f"Number of documents loaded: {len(docs)}")
    return docs

def load_and_process_pdf(file_path: str) -> Chroma:
    loader = PyPDFLoader(file_path, extract_images=False)
    pages = loader.load_and_split(text_splitter=CharacterTextSplitter())
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return Chroma.from_documents(pages, embeddings)

def load_azure_blob_container(azure_con_str, containername, filename):
    loader = AzureBlobStorageFileLoader(conn_str=azure_con_str, container=containername, blob_name=filename)
    
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = FakeEmbeddings(size=1536)
    return Chroma.from_documents(texts, embeddings)

def load_and_process_document(file_path: str) -> Chroma:
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = FakeEmbeddings(size=1536)
    return Chroma.from_documents(texts, embeddings)

def process_document(doc_load: list) -> Chroma:
    documents = doc_load 
    embeddings = FakeEmbeddings(size=1536)
    return Chroma.from_documents(documents, embeddings)





def run_conversational_retrieval_chain(docsearch: Chroma, question: str, chat_history: List[str]) -> str:
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY),
        retriever=docsearch.as_retriever(search_kwargs={"k": 1})
    )
    return chain.run(question=question, chat_history=chat_history)
