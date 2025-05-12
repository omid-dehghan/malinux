from Develops.Deepwork.duration import DurationList
import os
import json


class DataStorage:

    def __init__(self, config):
        self._config = config
        self.setPath(self.config.get_filepath())

    def load(self):
        if not os.path.exists(self.path) or os.path.getsize(self.path) == 0:
            return {}
        with open(self.path, "r") as f:
            raw_data = json.load(f)
            return {k: DurationList.from_list(v) for k, v in raw_data.items()}

    def save(self, data):
        serializable_data = {
            k: v.to_list() if hasattr(v, "to_list") else v
            for k, v in data.items()
        }
        with open(self.path, "w") as f:
            json.dump(serializable_data, f, indent=2)

    def setPath(self, path):
        self._path = path
    
    @property
    def path(self):
        return self._path
    
    @property
    def config(self):
        return self._config