from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_mistralai import ChatMistralAIc
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

#loading text file in memory...
loader = TextLoader(
    "D:\MODELS\LocalModel001\TinyLAMA\employee_handbook.txt",
    encoding = "utf-8"
)
docs = loader.load()
if docs:
    print("document load into memory...", type(docs))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 20
    )
    chunks = splitter.split_documents(docs)
    print("len of chunks is : ", len(chunks))
else:
    print('Docs not loaded...')


#loading model into memory...
embedding_model = HuggingFaceEmbeddings()

vectorstores = Chroma.from_documents(chunks, embedding_model)
if vectorstores:
    print('vectorstore created into RAM...')
else:
    print('vectorstore not created...')

# similarity search 
similar_retriever = vectorstores.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k":2}
)
print("============similarity_search serach Results====================")
similar_docs = similar_retriever.invoke("What GPA is required for scholarships?")
for doc in similar_docs:
    print(doc.page_content)


# MMR maximum marginal relevance
mmr_retriever = vectorstores.as_retriever(
    search_type = "mmr",
    search_kwargs = {"k":2}
)
print("============MMR serach Results====================")
mmr_docs = mmr_retriever.invoke("What GPA is required for scholarships?")
for doc in mmr_docs:
    print(doc.page_content)


#loaidng llm into memory...
llm = ChatMistralAI(
    model_name = "mistral-medium-3-5",
    temperature= 0.3
)

mqr_retriever = vectorstores.as_retriever()
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=mqr_retriever,
    llm=llm
)
result = multi_query_retriever.invoke("What GPA is required for scholarships?")
print("===============multiQuery Retriver response===================")
for doc in result:
    print(doc.page_content)