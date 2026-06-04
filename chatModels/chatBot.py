from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

load_dotenv()

model = ChatMistralAI(
    model_name = "mistral-medium-3-5",
    temperature= 0.9
)

choice = int(input("Enter you response: "))

if choice == 1:
    mode = "You are a Angry and frustated AI agent"
elif choice == 2:
    mode = "You are a funny AI agent"
elif choice == 3:
    mode = "You are a Sad AI agent"


message = [
    SystemMessage(content = mode)
]

print("-----------------Welcome to chatBot and Press 0 to exit-------------------------------")
while True:
    prompt = input("You : ")
    message.append(HumanMessage(content = prompt))
    if prompt == "0":
        break
    response = model.invoke(message)
    message.append(AIMessage(content = response.content))
    print("Bot : ", response.content)