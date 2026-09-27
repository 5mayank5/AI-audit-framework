import csv
import yaml

class CSVExporter:

    def __init__(self):
        with open("config.yaml") as f:
            self.config = yaml.safe_load(f)

    def export(self, data):
        with open(self.config["report"]["csv_output"], "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Agent", "Score"])

            for detail in data["heuristic_breakdown"]:
                writer.writerow([detail["agent"], detail["score"]])