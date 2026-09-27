import matplotlib.pyplot as plt
import numpy as np

# Models
models = ["Mistral", "Phi-3", "Gemma-2B", "LLaMA-3"]

# Metrics
adversarial = [0.9, 0.8, 1.0, 1.0]
toxicity_f1 = [0.567, 0.462, 0.651, 0.440]
bias_f1 = [0.214, 0.214, 0.077, 0.214]

x = np.arange(len(models))
width = 0.25

plt.figure()

plt.bar(x - width, adversarial, width, label="Adversarial")
plt.bar(x, toxicity_f1, width, label="Toxicity F1")
plt.bar(x + width, bias_f1, width, label="Bias F1")

plt.xlabel("Models")
plt.ylabel("Score")
plt.title("Model-wise Comparison of Safety Evaluation Metrics")

plt.xticks(x, models)
plt.legend()

plt.tight_layout()
plt.savefig("fig3_metrics_comparison.png", dpi=300)

plt.show()