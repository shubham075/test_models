from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
import torch


load_dotenv()

# load embedding model...
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# model_id = "microsoft/Phi-4-mini-instruct"
# model_id = "hieupt/TinyLlama-1.1B-Chat-v1.0-Q4_K_M-GGUF"
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype=torch.float16,
    device_map="auto"
)

pipe = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=250
)

llm = HuggingFacePipeline(pipeline=pipe)
if llm:
    print("call successfully...")
else:
    print("Calling Failed...")

