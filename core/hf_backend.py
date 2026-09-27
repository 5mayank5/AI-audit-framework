from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from core.model_interface import BaseModelBackend

class HFBackend(BaseModelBackend):

    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=120,
                do_sample=False
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)