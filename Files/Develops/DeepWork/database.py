from Develops.DeepWork.duration import DurationList
from Develops.DeepWork.helpers import Helper
from datetime import date
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
        serializable_data = {
            k: v.to_list() if hasattr(v, "to_list") else v
            for k, v in self.get_data().items()
        }
        with open(self.file_path, "w") as f:
            json.dump(serializable_data, f, indent=2)

    def initialize_total(self):
        total = Helper.dur_timedelta_obj("00:00")
        if "total" not in self.get_data():
            for key in self.get_data().keys():
                if not self.get_data()[key].isEmpty():
                    total += Helper.dur_timedelta_obj(
                        self.get_data()[key].get_total_duration)
            self.get_data()[
                "total"] = f"~{Helper.formatted_duration(total)}"
        self._save()

    def add(self, duration: str, index=None, target_date=str(date.today())):
        if target_date not in self.get_data():
            self.get_data()[target_date] = DurationList()
        self.total_duration("add", duration)
        self.get_data()[target_date].add(duration, index=index)
        self._save()

    def add_list(self, lst: list, target_date=str(date.today())):
        if target_date not in self.get_data():
            self.get_data()[target_date] = DurationList()
        for l in lst:
            self.total_duration("add", l)
            self.get_data()[target_date].add(l, index=None)
        self._save()

    def pop(self, index=-2, target_date=str(date.today())):
        if target_date not in self.get_data():
            raise IndexError(f"This date has no record: {target_date}")
        elif self.get_data()[target_date].isEmpty():
            raise IndexError(
                f"Records for this date are deleted: {target_date}")
        pop_item = self.get_data()[target_date].pop(index=index)
        self.total_duration("sub", str(pop_item))
        self._save()

    def pop_all(self, target_date=str(date.today())):
        if target_date not in self.get_data():
            raise IndexError(f"This date has no record: {target_date}")
        elif self.get_data()[target_date].isEmpty():
            raise IndexError(
                f"Records for this date are deleted: {target_date}")
        self.total_duration("sub", self.get_data()[
                            target_date].get_total_duration)
        self.get_data()[target_date] = DurationList()
        self._save()

    def total_duration(self, addorsub: str, duration: str):
        self.initialize_total()
        if addorsub.lower() == "add":
            total = Helper.dur_timedelta_obj(self.get_data()[
                "total"][1:])
            total += Helper.dur_timedelta_obj(duration)
            self.get_data()[
                "total"] = f"~{Helper.formatted_duration(total)}"
        elif addorsub.lower() == "sub":
            total = Helper.dur_timedelta_obj(self.get_data()[
                "total"][1:])
            total -= Helper.dur_timedelta_obj(duration)
            self.get_data()[
                "total"] = f"~{Helper.formatted_duration(total)}"

    def reset_total(self):
        if "total" in self.get_data():
            del self.get_data()["total"]
        self.initialize_total()
        return self.get("total")

    def get_info(self, index=None, start_date=None, end_date=str(date.today())):
        if index != None and index < 1:
            raise Exception(f"index should be greater than 0: {index}")
        if index != None:
            start_date = Helper.date_minus_days(end_date, index - 1)
        elif start_date == None and index == None:
            start_date = self.first_recorded_date()   
        return Helper.info(*self.get_records(start_date, end_date))

    def get(self, target_date=None):
        if target_date is None:
            target_date = str(date.today())
        else:
            return self.get_data().get(target_date, f"There is no record for this date: {target_date}")

    def get_data_len(self, target_date=None):
        if target_date is None:
            target_date = str(date.today())
        return len(self.get_data()[target_date])

    def get_data(self):
        return self.data

    def get_today_data(self):
        return self.get_data()[str(date.today())]

    def get_records(self, start_date, end_date):
        total = Helper.dur_timedelta_obj("00:00")
        date_pointer = start_date
        recorded_dates = 0
        total_days = 0
        while Helper.to_date(date_pointer) <= Helper.to_date(end_date):
            if date_pointer in self.get_data():
                if not self.get_data()[date_pointer].isEmpty():
                    total += Helper.dur_timedelta_obj(
                        self.get_data()[date_pointer].get_total_duration)
                    recorded_dates += 1
            total_days += 1
            date_pointer = Helper.next_day(date_pointer)
        return start_date, end_date, recorded_dates, total_days, total

    def first_recorded_date(self):
        d = str(date.today())
        for key in self.get_data().keys():
            if key != "total":
                d = Helper.earlier_date(d, key)
        return d