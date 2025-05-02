from datetime import timedelta, datetime


class Helper:

    @staticmethod
    def formatted_duration(td: timedelta):
        hours, minutes = Helper.from_timedelta(td)
        return f"{hours}:{minutes:02}"

    @staticmethod
    def dur_timedelta_obj(duration: str):
        hours, minutes = map(int, duration.split(":"))
        return timedelta(hours=hours, minutes=minutes)

    @staticmethod
    def from_timedelta(td: timedelta):
        total_minutes = int(td.total_seconds() // 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return hours, minutes

    @staticmethod
    def to_date(date: str):
        return datetime.strptime(date, '%Y-%m-%d').date()

    @staticmethod
    def previous_day(day: str):
        day = Helper.to_date(
            day)
        day -= timedelta(days=1)
        return str(day)

    @staticmethod
    def next_day(day: str):
        day = Helper.to_date(
            day)
        day += timedelta(days=1)
        return str(day)

    @staticmethod
    def date_minus_days(date: str, num: int):
        date = Helper.to_date(
            date)
        date -= timedelta(days=num)
        return str(date)

    @staticmethod
    def date_minus_date(date1: str, date2: str):
        date1 = Helper.to_date(
            date1)
        date2 = Helper.to_date(
            date2)
        return date2 - date1 + timedelta(days=1)

    @staticmethod
    def info(start_date, end_date, recorded_dates, total_days, total):
        percentage = recorded_dates / total_days * 100
        average = total / total_days
        hours, minutes = Helper.from_timedelta(average)
        return f"from:\t\t{start_date}\nto:\t\t{end_date}\nperformance:\t{recorded_dates} days out of {total_days}\npercentage:\t{int(percentage)}% of days\naverage:\t{hours}h {minutes}m\ntotal:\t\t~{Helper.formatted_duration(total)}"

    @staticmethod
    def sortDates(date1, date2):
        """
    Takes two date inputs (as datetime objects or ISO strings),
    returns a tuple: (earlier_date, later_date)
    """
    # Convert strings to datetime if needed
        if isinstance(date1, str):
            date1 = Helper.to_date(date1)
        if isinstance(date2, str):
            date2 = Helper.to_date(date2)
        return (str(date1), str(date2)) if date1 <= date2 else (str(date2), str(date1))

    @staticmethod
    def earlier_date(date1, date2):
        if isinstance(date1, str):
            date1 = Helper.to_date(date1)
        if isinstance(date2, str):
            date2 = Helper.to_date(date2)
        return str(date1) if date1 <= date2 else str(date2)
