from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# load embedding model...
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# load datasets...
loader = PyPDFLoader("D:\MODELS\LocalModel001\RAG_PIPELINE/test.pdf")
docs = loader.load()

# creating splitter and split docs into chunks...
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
chunks = splitter.split_documents(docs)
if chunks:
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="../chroma_DB_01"
    )
    print("chunks stored into vector DB...")
else:
    print("No chunks created...")
