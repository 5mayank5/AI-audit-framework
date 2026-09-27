import json
import platform
import datetime
import torch

class ExperimentLogger:

    def collect_environment(self):
        return {
            "timestamp": str(datetime.datetime.now()),
            "python_version": platform.python_version(),
            "torch_version": torch.__version__,
            "processor": platform.processor()
        }

    def save(self, env_data):
        with open("outputs/experiment_log.json", "w") as f:
            json.dump(env_data, f, indent=4)