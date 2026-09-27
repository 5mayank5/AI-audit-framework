import matplotlib.pyplot as plt
import yaml

class HTMLReportGenerator:

    def __init__(self):
        with open("config.yaml") as f:
            self.config = yaml.safe_load(f)

    def generate(self, scored_data):

        agents = [d["agent"] for d in scored_data["details"]]
        scores = [d["score"] for d in scored_data["details"]]

        plt.figure()
        plt.bar(agents, scores)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("outputs/score_graph.png")

        html = f"""
        <html>
        <body>
        <h1>AI Audit Report</h1>
        <h2>Total Score: {scored_data['total_score']}</h2>
        <h3>Severity: {scored_data['severity']}</h3>
        <img src="score_graph.png">
        </body>
        </html>
        """

        with open(self.config["report"]["html_output"], "w") as f:
            f.write(html)