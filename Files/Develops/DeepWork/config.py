import json
import os


class Config:
    def __init__(self, path=r"Files\Develops\Deepwork\config.json"):
        self.path = path
        self.data = {}
        self.defaults = {
            "filepath": os.path.join(os.path.expanduser("~"), "Desktop"),
            "filename": "deepwork"
        }
        if not os.path.exists(self.path):
            self.save(self.defaults)
        self.config = self.load()
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self, config_data=None):
        if config_data is None:
            config_data = self.config
        with open(self.path, "w") as f:
            json.dump(config_data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        if key not in self.data:
            raise KeyError(f"'{key}' is not a valid config key.")

        if key == "filepath" and not self.path_exists(value):
            raise ValueError(f"Invalid path: '{value}' does not exist.")

        self.data[key] = value
        self.save()
        return value

    def path_exists(self, path):
        return os.path.exists(path)
