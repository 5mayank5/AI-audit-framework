import json
import yaml

class JSONExporter:

    def __init__(self):
        with open("config.yaml") as f:
            self.config = yaml.safe_load(f)

    def export(self, data):
        with open(self.config["report"]["json_output"], "w") as f:
            json.dump(data, f, indent=4)