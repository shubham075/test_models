import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embedding_model

def build_vector_db(pdf_path: str, persist_dir: str):
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return None

    # Load embedding model
    emb_model = get_embedding_model()

    # Load dataset
    print(f"Loading document: {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # Creating splitter and split docs into chunks
    print("Splitting document into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    if chunks:
        print(f"Storing {len(chunks)} chunks into vector DB at '{persist_dir}'...")
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=emb_model,
            persist_directory=persist_dir
        )
        print("Chunks stored successfully!")
        return vectorstore
    else:
        print("No chunks created.")
        return None

# Only runs if executed directly (e.g. python create_database.py)
if __name__ == "__main__":
    pdf_file = r"D:\CODES\MODELS\RAG PIPELINE\test_models\RAG_PIPELINE\test.pdf"
    db_directory = "chroma_DB_01"
    build_vector_db(pdf_file, db_directory)
