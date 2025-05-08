from Develops.DeepWork.helpers import Helper
from Develops.DeepWork.database import Database
from datetime import date

class DataAnalyzer:
    def __init__(self, db: Database):
        self.db = db

    def first_recorded_date(self):
        dates = [d for d in self.db.get_data().keys() if d != "total"]
        return min(dates, default=str(date.today()), key=Helper.to_date)

    def get_info(self, index=None, start_date=None, end_date=str(date.today())):
        if index is not None:
            if index < 1:
                raise ValueError("Index should be >= 1")
            start_date = Helper.date_minus_days(end_date, index - 1)
        elif start_date is None:
            start_date = self.first_recorded_date()
        return Helper.info(*self.get_records(start_date, end_date))

    def get_records(self, start_date, end_date):
        total = Helper.dur_timedelta_obj("00:00")
        recorded_dates = 0
        total_days = 0
        pointer = start_date
        while Helper.to_date(pointer) <= Helper.to_date(end_date):
            record = self.db.get_data().get(pointer)
            if record and not record.isEmpty():
                total += Helper.dur_timedelta_obj(record.get_total_duration)
                recorded_dates += 1
            total_days += 1
            pointer = Helper.next_day(pointer)
        return start_date, end_date, recorded_dates, total_days, total
