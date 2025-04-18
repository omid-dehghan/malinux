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
        serializable_data = {
        k: v.to_list() if hasattr(v, "to_list") else v
        for k, v in self.get_data().items()
    }
        with open(self.file_path, "w") as f:
            json.dump(serializable_data, f, indent=2)

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

    def pop(self,index = -2, target_date=str(date.today())):
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
        self.total_duration("sub", self.get_data()[target_date].get_total_duration)
        self.get_data()[target_date] = DurationList()
        self._save()
        
    def total_duration(self, addorsub:str, duration:str):
        total = DurationList.Duration.get_timedelta_obj("00:00")
        if "total" not in self.get_data():
            for key in self.get_data().keys():
                if not self.get_data()[key].isEmpty() : 
                    total += DurationList.Duration.get_timedelta_obj(self.get_data()[key].get_total_duration)
            self.get_data()["total"] = f"~{DurationList.Duration.from_timedelta(total)}"
        if addorsub.lower() == "add":
            total = DurationList.Duration.get_timedelta_obj(self.get_data()["total"][1:])
            total += DurationList.Duration.get_timedelta_obj(duration)
            self.get_data()["total"] = f"~{DurationList.Duration.from_timedelta(total)}"
        if addorsub.lower() == "sub":
            total = DurationList.Duration.get_timedelta_obj(self.get_data()["total"][1:])
            total -= DurationList.Duration.get_timedelta_obj(duration)
            self.get_data()["total"] = f"~{DurationList.Duration.from_timedelta(total)}"


    def get(self, target_date=None):
        if target_date is None:
            target_date = str(date.today())
        return self.get_data().get(target_date, f"There is no record for this date: {target_date}")

    def get_data_len(self, target_date=None):
        if target_date is None:
            target_date = str(date.today())
        return len(self.get_data()[target_date])

    def get_data(self):
        return self.data

    def get_today_data(self):
        return self.get_data()[str(date.today())] 

if __name__ == "__main__":
    try:
        pass
    except Exception as e:
        print(e)
