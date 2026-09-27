import matplotlib.pyplot as plt
import numpy as np


class RiskVisualizer:

    def generate(self, result):

        components = result["risk_components"]

        labels = list(components.keys())
        values = list(components.values())

        # Radar chart requires closing the circle
        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

        ax.plot(angles, values, linewidth=2)
        ax.fill(angles, values, alpha=0.25)

        ax.set_thetagrids(np.degrees(angles[:-1]), labels)

        ax.set_title("AI Model Risk Profile")

        plt.savefig("outputs/risk_radar.png")
        plt.close()