import yaml
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def load_model(model_name):

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if "t5" in model_name or "bart" in model_name:
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        model_type = "seq2seq"
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        model_type = "causal"

    model.eval()

    return {
        "model": model,
        "tokenizer": tokenizer,
        "model_type": model_type
    }

