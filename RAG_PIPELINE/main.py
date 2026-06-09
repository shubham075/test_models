from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from create_database import vectorstore
from ModelCALL import llm, embedding_model
import torch
import time


load_dotenv()

#loading llm into memory...
# llm = ChatMistralAI(
#     model_name = "mistral-medium-3-5",
#     temperature= 0.3
# )

retriever_response = vectorstore.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            "k":5,
            "fetch_k":10,
            "lambda_mult":0.5
        }
    )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a helpful AI assistant.
        Use only provided context to answer the question.
        If the answer is not present in the context, say: 'I could not find the answer in the documnet.'
        """),
        ("human", """Context: {context}
        Question: {question}""")
    ]
)

print("RAG system created...")
print("Press 0 to exit : ")
while True:
    query = input("You : ")
    if query == "0":
        break

    docs = retriever_response.invoke(query)

    # build context using retrived documents(docs)
    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt.invoke(
        {
            "context":context,
            "question":query
        }
    )
    start_time = time.perf_counter()
    response = llm.invoke(final_prompt)
    print("\n\n AI : ", response)
    end_time = time.perf_counter()

    print(f"\nResponse Time: {end_time - start_time:.2f} seconds")


