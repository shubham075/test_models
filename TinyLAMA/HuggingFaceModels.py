from dotenv import load_dotenv
import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

load_dotenv()
# model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model_id = "microsoft/Phi-4-mini-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype=torch.float16,
    device_map="auto"
)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=100
)
start_time = time.perf_counter()
response = pipe("Hello, how are you?")
end_time = time.perf_counter()
print(response[0]["generated_text"])


# from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
# llm = HuggingFacePipeline.from_model_id(
#     model_id = model_id,
#     task = "text-generation",
#     pipeline_kwargs={
#         "max_new_tokens": 100,
#         "temperature": 0.1,
#     }
# )
# chat_model = ChatHuggingFace(llm=llm)

# start_time = time.perf_counter()
# response = chat_model.invoke('Hi, Are you there?')
# print(response.content)
# end_time = time.perf_counter()


print(f"\nResponse Time: {end_time - start_time:.2f} seconds")