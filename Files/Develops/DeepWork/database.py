from Develops.Deepwork.helpers import Helper
from Develops.Deepwork.duration import DurationList
from Develops.Deepwork.storage import DataStorage
from datetime import date


class Database:
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self.reload()
    
    def reload(self):
        self.data = self.storage.load()

    def save(self):
        self.storage.save(self.data)
    
    def perform_action(self, action, **kargs):
        actions = {"add": self.add_duration,
                   "pop": self.pop_duration,
                   "popall": self.pop_all_duration,
                   "today": self.get_today_data,
                   "addlist": self.add_list,
                   "clearalldata": self.clear_alldata,
                   "get": self.get,
                   "alldata": self.get_data
                   }
        result = actions[action](**kargs)
        self.reset_total()
        return result

    def initialize_total(self):
        total = Helper.dur_timedelta_obj("00:00")
        if "total" not in self.data:
            for key, val in self.data.items():
                if key == "total" or val.isEmpty():
                    continue
                total += Helper.dur_timedelta_obj(val.get_total_duration)
            self.data["total"] = f"~{Helper.formatted_duration(total)}"
        self.save()
        
    def add_duration(self, duration: str, index=None, target_date=str(date.today())):
        if target_date not in self.data:
            self.data[target_date] = DurationList()
        self.data[target_date].add(duration, index=index)
        self.save()
        return self.get(target_date)

    def add_list(self, durations: list, target_date=str(date.today())):
        if target_date not in self.data:
            self.data[target_date] = DurationList()
        for d in durations:
            self.add_duration(d, None, target_date)
        self.save()
        return self.get(target_date)

    def pop_duration(self, index=-2, target_date=str(date.today())):
        if target_date not in self.data or self.data[target_date].isEmpty():
            raise IndexError(f"No valid record for date: {target_date}")
        self.data[target_date].pop(index=index)
        self.save()
        return self.get(target_date)

    def pop_all_duration(self, target_date=str(date.today())):
        if target_date not in self.data or self.data[target_date].isEmpty():
            raise IndexError(
                f"No valid records to pop for date: {target_date}")
        self.data[target_date] = DurationList()
        self.save()
        return self.get(target_date)

    def reset_total(self):
        self.data.pop("total", None)
        self.initialize_total()
        return self.data["total"]

    def get_dates_and_durations(self):
        dates = []
        durations = []
        pointer = Helper.first_recorded_date(self.get_data())
        while Helper.to_date(pointer) <= Helper.to_date(str(date.today())):
            if pointer != "total":
                dates.append(pointer)
                if pointer not in self.data or self.data[pointer].isEmpty():
                    durations.append(Helper.timedelta_to_min(
                        Helper.dur_timedelta_obj("00:00")))
                else:
                    durations.append(Helper.timedelta_to_min(
                        Helper.dur_timedelta_obj(self.data[pointer].get_total_duration)))
            pointer = Helper.next_day(pointer)
        return dates, durations

    def get(self, target_date=None):
        if target_date is None:
            target_date = str(date.today())
        if target_date in self.data:
            return self.data[target_date]
        return f"There is no record for this date: {target_date}"
    
    def clear_alldata(self):
        self.data = {}
        self.save()
        return "Done"

    def get_data(self):
        return self.data

    def get_today_data(self):
        return self.data.get(str(date.today()), DurationList())

    def get_data_len(self, target_date=None):
        return len(self.get_today_data() if target_date is None else self.data.get(target_date, []))
