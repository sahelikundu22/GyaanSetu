import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "ai4bharat/IndicBART",
    do_lower_case=False,
    use_fast=False,
    keep_accents=True
)

# Load model
model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/IndicBART")
model.eval()

# Special token ids
bos_id = tokenizer._convert_token_to_id_with_added_voc("<s>")
eos_id = tokenizer._convert_token_to_id_with_added_voc("</s>")
pad_id = tokenizer._convert_token_to_id_with_added_voc("<pad>")



def ask_model(question, context):

    # keep prompt simple
    prompt = f"{context}\nQuestion: {question}\nAnswer:"

    formatted_input = f"{prompt} </s> <2en>"

    inputs = tokenizer(
        formatted_input,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )

    with torch.no_grad():
        output = model.generate(
            inputs.input_ids,
            num_beams=4,
            max_length=60,
            early_stopping=True,
            pad_token_id=pad_id,
            bos_token_id=bos_id,
            eos_token_id=eos_id,
            decoder_start_token_id=tokenizer._convert_token_to_id_with_added_voc("<2en>")
        )

    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

    decoded_output = decoded_output.replace("<2en>", "").strip()

    return decoded_output

  