from abc import ABC, abstractmethod
import time
import torch
from core.injection_detector import PromptInjectionDetector


class BaseAgent(ABC):

    def __init__(self, model_bundle, config):
        """
        model_bundle = {
            "model": AutoModelForCausalLM,
            "tokenizer": AutoTokenizer
        }
        """
        self.model = model_bundle["model"]
        self.tokenizer = model_bundle["tokenizer"]
        self.config = config
        self.detector = PromptInjectionDetector()

    @abstractmethod
    def get_prompts(self):
        pass

    def run(self):

        start_time = time.time()
        results = []
        injection_flags = 0

        for prompt in self.get_prompts():

            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt"
            )

            # Disable gradient computation (important for CPU efficiency)
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=60,
                    do_sample=False,  # deterministic decoding
                    pad_token_id=self.tokenizer.eos_token_id
                )

            # Decode generated output
            output_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )

            # Injection detection
            if self.detector.detect(output_text):
                injection_flags += 1

            results.append({
                "prompt": prompt,
                "response": output_text
            })

        execution_time = round(time.time() - start_time, 3)

        return {
            "agent_name": self.__class__.__name__,
            "execution_time": execution_time,
            "injection_flags": injection_flags,
            "results": results
        }