from Develops.DeepWork.duration import DurationList
import os
import json

class DataStorage:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return {}
        with open(self.file_path, "r") as f:
            raw_data = json.load(f)
            return {k: DurationList.from_list(v) for k, v in raw_data.items()}

    def save(self, data):
        serializable_data = {
            k: v.to_list() if hasattr(v, "to_list") else v
            for k, v in data.items()
        }
        with open(self.file_path, "w") as f:
            json.dump(serializable_data, f, indent=2)
