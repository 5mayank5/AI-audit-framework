import json
import torch
from core.metrics import compute_metrics


class DatasetToxicityAgent:

    def __init__(self, model_bundle, config, dataset_path):
        self.model = model_bundle["model"]
        self.tokenizer = model_bundle["tokenizer"]
        self.dataset_path = dataset_path
        self.unsafe_keywords = config["scoring"]["unsafe_keywords"]

    def detect_unsafe(self, text):
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.unsafe_keywords)

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

            predicted_toxic = self.detect_unsafe(output_text)
            is_toxic = true_label == "toxic"

            if predicted_toxic and is_toxic:
                TP += 1
            elif predicted_toxic and not is_toxic:
                FP += 1
            elif not predicted_toxic and is_toxic:
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