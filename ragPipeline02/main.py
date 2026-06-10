import time
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from model_call import llm, embedding_model
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

persist_directory = "chroma_DB_01"
vectorstore = Chroma(
    persist_directory=persist_directory, embedding_function=embedding_model
)

retriever_response = vectorstore.as_retriever(
    search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10, "lambda_mult": 0.5}
)

print("\nRAG system initialized successfully from disk!")
print("Press '0' to exit.\n")

while True:
    query = input("You : ").strip()
    if query == "0":
        print("Goodbye!")
        break
    if not query:
        continue

    # Retrieve context
    docs = retriever_response.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Create LangChain messages
    messages = [
        SystemMessage(
            content="You are a helpful AI assistant. Use only the provided context to answer the question. If the answer is not present in the context, say: 'I could not find the answer in the documnet.'"
        ),
        HumanMessage(
            content=f"Context:\n{context}\n\nQuestion: {query}\n\nRemember: Answer based ONLY on the context. If the answer is not present, say 'I could not find the answer in the documnet.'"
        )
    ]

    # Convert LangChain messages to the format expected by the tokenizer chat template
    formatted_messages = [
        {"role": "system" if isinstance(msg, SystemMessage) else "user", "content": msg.content}
        for msg in messages
    ]
    tokenizer = llm.pipeline.tokenizer
    final_prompt = tokenizer.apply_chat_template(
        formatted_messages, tokenize=False, add_generation_prompt=True
    )

    start_time = time.perf_counter()
    response = llm.invoke(final_prompt)
    end_time = time.perf_counter()

    print(f"\nAI : {response.strip()}")
    print(f"\nResponse Time: {end_time - start_time:.2f} seconds\n")
