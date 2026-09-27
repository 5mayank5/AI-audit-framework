from .base_agent import BaseAgent
import json

class DatasetAgent(BaseAgent):

    def __init__(self, model, config, dataset_path):
        super().__init__(model, config)
        self.dataset_path = dataset_path

    def get_prompts(self):
        with open(self.dataset_path) as f:
            self.dataset = json.load(f)
        return [item["prompt"] for item in self.dataset]