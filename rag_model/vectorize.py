import configparser
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings

config = configparser.ConfigParser()
config.read("config.ini")

def embed_and_save(file: str) -> str:
    docs = PyMuPDFLoader(f"./docs/{file}").load()
    text_split = RecursiveCharacterTextSplitter(chunk_size=1000)
    split_docs = text_split.split_documents(docs)
    embedding_model = HuggingFaceEmbeddings(model_name=config['AI']['embedding'])
    Chroma.from_documents(split_docs, embedding_model, persist_directory="./vectorstore")
    return 'Added new doc successfully!'