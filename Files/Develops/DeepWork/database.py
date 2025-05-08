from Develops.DeepWork.helpers import Helper
from Develops.DeepWork.duration import DurationList
from Develops.DeepWork.storage import DataStorage
from datetime import date


class Database:
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self.data = self.storage.load()

    def save(self):
        self.storage.save(self.data)

    def initialize_total(self):
        total = Helper.dur_timedelta_obj("00:00")
        if "total" not in self.data:
            for key, val in self.data.items():
                if key == "total" or val.isEmpty():
                    continue
                total += Helper.dur_timedelta_obj(val.get_total_duration)
            self.data["total"] = f"~{Helper.formatted_duration(total)}"
        self.save()

    def total_duration(self, action, duration):
        self.initialize_total()
        total = Helper.dur_timedelta_obj(self.data["total"][1:])
        change = Helper.dur_timedelta_obj(duration)
        total = total + change if action == "add" else total - change
        self.data["total"] = f"~{Helper.formatted_duration(total)}"

    def add_duration(self, duration: str, index=None, target_date=str(date.today())):
        if target_date not in self.data:
            self.data[target_date] = DurationList()
        self.total_duration("add", duration)
        self.data[target_date].add(duration, index=index)
        self.save()

    def add_list(self, durations: list, target_date=str(date.today())):
        if target_date not in self.data:
            self.data[target_date] = DurationList()
        for d in durations:
            self.add_duration(d, None, target_date)
        self.save()

    def pop_duration(self, index=-2, target_date=str(date.today())):
        if target_date not in self.data or self.data[target_date].isEmpty():
            raise IndexError(f"No valid record for date: {target_date}")
        pop_item = self.data[target_date].pop(index=index)
        self.total_duration("sub", str(pop_item))
        self.save()

    def pop_all_duration(self, target_date=str(date.today())):
        if target_date not in self.data or self.data[target_date].isEmpty():
            raise IndexError(
                f"No valid records to pop for date: {target_date}")
        self.total_duration("sub", self.data[target_date].get_total_duration)
        self.data[target_date] = DurationList()
        self.save()

    def reset_total(self):
        self.data.pop("total", None)
        self.initialize_total()
        return self.data["total"]
    
    def get(self, target_date=None):
        if target_date is None:
            target_date = str(date.today())
        if target_date in self.data:
            return self.data[target_date]
        return f"There is no record for this date: {target_date}"
    
    def get_data(self):
        return self.data

    def get_today_data(self):
        return self.data.get(str(date.today()), DurationList())

    def get_data_len(self, target_date=None):
        return len(self.get_today_data() if target_date is None else self.data.get(target_date, []))
