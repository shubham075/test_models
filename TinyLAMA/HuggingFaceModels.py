from dotenv import load_dotenv
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

load_dotenv()

llm = HuggingFacePipeline.from_model_id(
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task = "text-generation",
    pipeline_kwargs={
        "max_new_tokens": 100,
        "temperature": 0.1,
    }
)

chat_model = ChatHuggingFace(llm=llm)
response = chat_model.invoke("Hello, what can you do?")

print("response", response.content)

import torch

print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))