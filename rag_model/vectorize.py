import configparser
from PyPDF2 import PdfReader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

config = configparser.ConfigParser()
config.read("config.ini")

def get_pdf_text(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def embed_and_save(file: str) -> str:
    try:
        docs = get_pdf_text(file)
        text_split = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        split_docs = text_split.split_text(docs)
        embedding_model = HuggingFaceEmbeddings(model_name=config["AI"]["embedding"])
        Chroma.from_texts(split_docs, embedding_model)
        return "Added new document successfully!"
    except ValueError:
        return f"Can't find {file} in docs directory!"
    except:
        return "Error occured whiles performing embedding."

# , persist_directory="./vectorstore"