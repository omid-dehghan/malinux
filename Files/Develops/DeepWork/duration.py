from datetime import timedelta, datetime
from Develops.Deepwork.helpers import Helper
import re


class DurationList:

    def __init__(self):
        self._ls = []

    def add(self, duration, index: int, total_duration=False):
        duration = self.Duration(duration)
        if duration < DurationList.Duration.MIN_DURATION:
            raise ValueError(
                f"Duration cannot be zero or negetive (+{DurationList.Duration.MIN_DURATION})")
        if not self._ls or total_duration:
            self._ls.append(str(duration))
            self._ls.append(f"~{duration}")
        else:
            if index == None:
                index = len(self._ls) - 1
            tot = self.Duration(self._ls[len(self._ls) - 1][1:]) + duration
            self._ls.pop()
            self._ls.insert(index, str(duration))
            if self.Duration(tot) > self.Duration.MAX_DURATION:
                raise ValueError(f"You cannot work over 24 hours: {tot}")
            self._ls.append(f"~{tot}")

    def pop(self, index=-2):
        if self.isEmpty():
            raise IndexError("There is no deepwork record for this date...")
        elif len(self._ls) == 2:
            poped_item = self._ls[0]
            self._ls = []
            return poped_item
        elif index == -1 or index == len(self._ls) - 1:
            raise IndexError(f"index cannot be: {index}")
        else:
            poped_item = self.Duration(self._ls.pop(index))
            tot = poped_item - self.Duration(self._ls[len(self._ls) - 1][1:])
            self._ls[len(self._ls) - 1] = f"~{tot}"
            return poped_item

    @classmethod
    def from_list(cls, data):
        obj = cls()
        obj._ls = data
        return obj

    def isEmpty(self):
        return len(self._ls) == 0

    def to_list(self):
        return self._ls

    def __str__(self):
        return str(self._ls)

    def __repr__(self):
        return f"{self._ls}\n"
    
    def __getitem__(self, index):
        if index == len(self._ls) - 1:
            raise IndexError(f"There is no index {index}")
        return self._ls[index]

    def __len__(self):
        if len(self._ls) == 0:
            return 0
        else:
            return len(self._ls) - 1

    def __iter__(self):
        return iter(self._ls[:-1])

    @property
    def get_total_duration(self):
        return self.__getitem__(-1)[1:]

    # ================================================= Duration class

    class Duration:
        """class that implemented on datetime class\n
        Duration is an instance of 'datetime.timedelta' class"""
    # ================================ Class Attributes

        MAX_DURATION = timedelta(hours=24)
        MIN_DURATION = timedelta(hours=0, minutes=0, seconds=1)

    # ================================ Constructor

        def __init__(self, duration="0:00"):

            if not isinstance(duration, str):
                raise TypeError(
                    "Duration must be a string in 'HH:MM' or 'H:MM' format")

            if not re.match(r"^\d{1,2}:\d{2}$", duration):
                raise ValueError(
                    "Duration must be a string in 'HH:MM' or 'H:MM' format")

            hours, minutes = map(int, duration.split(":"))

            if minutes >= 60:
                raise ValueError("Minutes must be less than 60")

            self._duration = timedelta(hours=hours, minutes=minutes)

            if self._duration > self.MAX_DURATION:
                raise ValueError(
                    f"Duration cannot exceed {self._duration} (24 hours)")

        def __str__(self):
            hours = int(self.total_minutes // 60)
            minutes = int(self.total_minutes % 60)
            return f"{hours:02}:{minutes:02}"

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self._duration == other._duration
            elif isinstance(other, timedelta):
                return self._duration == other
            return NotImplemented

        def __ne__(self, other):
            eq = self.__eq__(other)
            if eq is NotImplemented:
                return NotImplemented
            return not eq

        def __lt__(self, other):
            if isinstance(other, self.__class__):
                return self._duration < other._duration
            elif isinstance(other, timedelta):
                return self._duration < other
            return NotImplemented

        def __le__(self, other):
            if isinstance(other, self.__class__):
                return self._duration <= other._duration
            elif isinstance(other, timedelta):
                return self._duration <= other
            return NotImplemented

        def __gt__(self, other):
            if isinstance(other, self.__class__):
                return self._duration > other._duration
            elif isinstance(other, timedelta):
                return self._duration > other
            return NotImplemented

        def __ge__(self, other):
            if isinstance(other, self.__class__):
                return self._duration >= other._duration
            elif isinstance(other, timedelta):
                return self._duration >= other
            return NotImplemented

        def __add__(self, other):
            if isinstance(other, self.__class__):
                total = other.duration + self._duration
                return Helper.formatted_duration(total)
            return NotImplemented

        def __sub__(self, other):
            if isinstance(other, self.__class__):
                total = other.duration - self.duration
                return Helper.formatted_duration(total)
            return NotImplemented

# ========================= properties

        @property
        def duration(self):
            return self._duration

        @property
        def total_seconds(self):
            return self._duration.total_seconds()

        @property
        def total_minutes(self):
            return self.total_seconds // 60


if __name__ == "__main__":
    pass
