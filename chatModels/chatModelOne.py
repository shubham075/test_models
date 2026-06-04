from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(
    model_name = "mistral-medium-3-5",
    temperature= 0.3
)
response = model.invoke("what can you do?")
print(response.content)

load_dotenv()
 