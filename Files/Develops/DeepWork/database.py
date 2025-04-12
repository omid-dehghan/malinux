from datetime import date
from Develops.DeepWork.duration import DurationList
import json
import os


class dateDB:
    def __init__(self):
        # File Path ==============
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.file_path = os.path.join(desktop_path, "deepwork.json")
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return {}
        with open(self.file_path, "r") as f:
            raw_data = json.load(f)
            return {k: DurationList.from_list(v) for k, v in raw_data.items()}

    def _save(self):
        serializable_data = {k: v.to_list() for k, v in self.data.items()}
        with open(self.file_path, "w") as f:
            json.dump(serializable_data, f, indent=2)

    def add(self, duration:str, index = None, target_date=str(date.today())):
        if target_date not in self.data:
            self.data[target_date] = DurationList()
        self.data[target_date].add(duration, index=index)
        self._save()

    def add_list(self, lst: list, target_date=str(date.today())):
        if target_date not in self.data:
            self.data[target_date] = DurationList()
        for l in lst:
            self.data[target_date].add(l, index=None)
        self._save()

    def pop(self, target_date=str(date.today())):
        if target_date not in self.data:
            raise IndexError(f"This date has no record: {target_date}")
        elif self.data[target_date].isEmpty():
            raise IndexError(f"Records for this date are deleted: {target_date}")
        self.data[target_date].pop()
        self._save()
        
    def pop_all(self, target_date=str(date.today())):
        if target_date not in self.data:
            raise IndexError(f"This date has no record: {target_date}")
        elif self.data[target_date].isEmpty():
            raise IndexError(f"Records for this date are deleted: {target_date}")
        self.data[target_date] = DurationList()
        self._save()

    def get(self, target_date=None):
        if target_date is None:
            target_date = str(date.today())
        return self.data.get(target_date, f"There is no record for this date: {target_date}")

    def get_data_len(self, target_date=None):
        if target_date is None:
            target_date = str(date.today())
        return len(self.get_data()[target_date])
    def get_data(self):
        return self.data
    
    def get_today_data(self):
        return self.get_data()[str(date.today())]




