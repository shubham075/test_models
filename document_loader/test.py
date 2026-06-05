from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

data = PyPDFLoader("document_loader/2312.10997v5.pdf")
docs = data.load()
# print(docs[0].page_content)

templets = ChatPromptTemplate.from_messages(
    [("system", "You are the AI that summarize the text."),
    ("human", "{data}")]
)

model = ChatMistralAI(
    model_name = "mistral-medium-3-5",
    temperature= 0.3
)
prompt = templets.format_messages(data = docs[0].page_content)
response = model.invoke(prompt)
print(response.content)