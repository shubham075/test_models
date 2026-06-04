from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

text_embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
text = [
    "Hello, how are you?",
    "What is the weather like today?",
    "What is the capital city of Madhya Pradesh?",
]

vector_list = text_embedding_model.embed_documents(text)
print(vector_list)
