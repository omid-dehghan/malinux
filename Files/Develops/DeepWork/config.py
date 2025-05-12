from Develops.Deepwork.database import DataStorage
import json
import os


class Config:
    def __init__(self, path=r"Files\Develops\Deepwork\config.json"):
        self.path = path
        self.data = {}
        self.defaults = {
            "path": f"{os.path.join(os.path.expanduser("~"), "Desktop")}\\",
            "filename": "deepwork"
        }
        if not os.path.exists(self.path):
            self.save(self.defaults)

        self.data = self.load()

        if not self.is_valid_config(self.data):
            print("Invalid or empty config, resetting to default.")
            self.data = self.defaults.copy()
            self.save(self.data)

    def load(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save(self, config_data=None):
        if config_data is None:
            config_data = self.data
        with open(self.path, "w") as f:
            json.dump(config_data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        if key not in self.data:
            raise KeyError(f"'{key}' is not a valid config key.")

        if key == "path" and not self.path_exists(value):
            raise ValueError(f"Invalid path: '{value}' does not exist.")

        self.data[key] = value
        self.save()
        return f"[✓] path changed: {self.get_filepath()}"

    def path_exists(self, path):
        return os.path.exists(path)

    def is_valid_config(self, config):
        if not config or not isinstance(config, dict):
            return False
        return all(key in config for key in self.defaults)

    def get_path(self):
        return self.data.get("path")

    def get_filename(self):
        return self.data.get("filename")

    def get_filepath(self):
        return f"{self.get_path() + self.get_filename()}.json"

    @property
    def ds(self):
        return self._ds
