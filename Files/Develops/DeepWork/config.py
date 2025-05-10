import json
import os

class Config:
    def __init__(self, path=r"Files\Develops\Deepwork\config.json"):
        self.path = path
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        if key not in self.data:
            raise Exception("config does not exist.")
        if key == "filepath":
            if self.path_exists(value):
                self.data[key] = value
                self.save()
            else:
                raise Exception(f"The path {value} does not exist.")
        elif key == "filename":
            self.data[key] = value
            self.save()


    def path_exists(self, path):
        return os.path.exists(path)