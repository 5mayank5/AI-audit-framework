import json
import torch
from core.metrics import compute_metrics


class DatasetBiasAgent:

    def __init__(self, model_bundle, config, dataset_path):
        self.model = model_bundle["model"]
        self.tokenizer = model_bundle["tokenizer"]
        self.dataset_path = dataset_path
        self.bias_keywords = config["scoring"]["bias_keywords"]

    def detect_bias(self, text):
        text_lower = text.lower()
        for keyword in self.bias_keywords:
            if keyword in text_lower:
                return True
        return False

    def run(self):

        with open(self.dataset_path, "r") as f:
            dataset = json.load(f)

        TP = FP = FN = 0

        for item in dataset:

            prompt = item["prompt"]
            true_label = item["label"]

            inputs = self.tokenizer(prompt, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=40,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            output_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )

            predicted_biased = self.detect_bias(output_text)
            is_biased = true_label == "biased"

            if predicted_biased and is_biased:
                TP += 1
            elif predicted_biased and not is_biased:
                FP += 1
            elif not predicted_biased and is_biased:
                FN += 1

        metrics = compute_metrics(TP, FP, FN)

        return {
            "TP": TP,
            "FP": FP,
            "FN": FN,
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1_score": metrics["f1_score"],
            "total_samples": len(dataset)
        }