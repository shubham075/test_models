from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
model = ChatMistralAI(
    model = "mistral-medium-3-5",
    temperature= 0.1
)

prompt = ChatPromptTemplate.from_messages([
    """Need to add strcutured prompts for better conntext..."""
])

user_input = input('Enter your paragraph: ')
final_prompt = prompt.invoke({"placeholder_varibale": user_input})

response = model.invoke(final_prompt)
print(response.content)