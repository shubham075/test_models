from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
import torch
from transformers import BitsAndBytesConfig
from create_database import get_embedding_model

load_dotenv()

# Get the embedding model instance
embedding_model = get_embedding_model()

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    # llm_int8_enable_fp32_cpu_offload=True
)

def get_llm():
    model_id = "microsoft/Phi-3-mini-4k-instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_id, clean_up_tokenization_spaces=False)
    # Ensure pad token is set to avoid warnings during generation
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        quantization_config=quantization_config,
        device_map="auto"
    )

    # Suppress the max_length / max_new_tokens warning by explicitly resetting max_length
    model.generation_config.max_length = None

    pipe = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=300,
        return_full_text=False,
        pad_token_id=tokenizer.eos_token_id
    )

    return HuggingFacePipeline(pipeline=pipe)

# Exporting instances
llm = get_llm()

if __name__ == "__main__":
    if llm:
        print("LLM loaded successfully...")
    else:
        print("Calling Failed...")
