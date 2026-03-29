import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-7B-Instruct"  # smaller & usable

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.float16,
    device_map="auto"
)

def ask_model(question, context):

    prompt = f"""
Answer the question using ONLY the context below.
Answer in the same language as the question (Hindi/Bengali if used).

Context:
{context}

Question:
{question}
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.2
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer