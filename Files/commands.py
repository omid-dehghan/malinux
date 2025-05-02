from datetime import datetime, date
from Develops.DeepWork.duration import DurationList
from Develops.DeepWork.database import dateDB
from Develops.DeepWork.database import Helper


class CommandValidator:
    MAIN_COMMANDS = ["deepwork",
                     "pop",
                     "popall",
                     "list",
                     "today",
                     "total",
                     "retotal"
                     ]

    def __init__(self):
        pass

    def validate(self, cmds):
        for cmd in cmds:
            if not (
                cmd in self.MAIN_COMMANDS
                or CommandValidator.is_date(cmd)
                or CommandValidator.is_duration(cmd)
                or CommandValidator.is_valid_index(cmd)
            ):
                raise CommandNotFoundException(cmd)
        self._cmds = cmds
        return True

    @staticmethod
    def is_duration(token):
        try:
            DurationList.Duration(token)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_date(token):
        try:
            datetime.strptime(token, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_index(token):
        """Check if token is a valid integer index, including negative indexes"""
        try:
            int(token)
            return True  # Allow both positive and negative integers
        except ValueError:
            return False

    @property
    def cmds(self) -> list:
        return self._cmds


class CommandExecutor:

    def __init__(self, db: dateDB):
        self._db = db

    def execute(self, cmds):
        self.setCommands(cmds)
        if self.cmds[0] == "deepwork":
            if self.command_exists(1) and CommandValidator.is_date(self.cmds[1]):
                return self.date_related_commands()
            elif self.len_commands > 2:
                return self.greater_than_two_commands()
            elif len(self.cmds) == 2:
                return self.two_layer_command()
            else:
                return "command not found"
        else:
            return f"command_not_found: <{self.cmds[0]}>: command not found"

    def one_layer_command(self):
        if self.cmds[0] == "deepwork":
            raise IncompleteCommandException(self.cmds[0])

    def two_layer_command(self):
        # pop commands
        cmd = self.cmds[1]
        if cmd == "pop":
            self.db.pop()
            return self.db.get_today_data()
        elif cmd == "popall":
            self.db.pop_all()
            return self.db.get_today_data()
        elif cmd == "today":
            return self.db.get_today_data()
        elif cmd == "total":
            return self.db.get_info()
        elif cmd == "retotal":
            return self.db.reset_total()
        elif CommandValidator.is_valid_index(self.cmds[1]):
            return self.db.get_info(int(self.cmds[1]))
        elif CommandValidator.is_duration(cmd):
            self.db.add(cmd)
            return self.db.get_today_data()
        else:
            return f"command_not_found: <{self.cmds[1]}>: command not found"

    def date_related_commands(self):
        # get data
        if CommandValidator.is_date(self.cmds[1]) and not self.command_exists(2):
            return self.db.get(self.cmds[1])
        # single duration append
        elif CommandValidator.is_date(self.cmds[1]) and CommandValidator.is_duration(self.cmds[2]) and not self.command_exists(3):
            self.db.add(target_date=self.cmds[1], duration=self.cmds[2])
            return self.db.get(self.cmds[1])
        # single duration insert
        elif CommandValidator.is_date(self.cmds[1]) and CommandValidator.is_duration(self.cmds[2]) and CommandValidator.is_valid_index(self.cmds[3]):
            self.db.add(
                target_date=self.cmds[1], duration=self.cmds[2], index=int(self.cmds[3]))
            return self.db.get(self.cmds[1])
        # single duration pop
        elif CommandValidator.is_date(self.cmds[1]) and self.cmds[2] == "pop":
            self.db.pop(target_date=self.cmds[1])
            return self.db.get(self.cmds[1])
        # single pop indexed
        elif CommandValidator.is_date(self.cmds[1]) and self.cmds[2] == "pop" and CommandValidator.is_valid_index(self.cmds[3]):
            self.db.pop(int(self.cmds[3]))
            return self.db.get(self.cmds[1])
        # pop all
        elif CommandValidator.is_date(self.cmds[1]) and self.cmds[2] == "popall":
            self.db.pop_all(target_date=self.cmds[1])
            return self.db.get(self.cmds[1])
        # list append
        elif CommandValidator.is_date(self.cmds[1]) and self.cmds[2] == "list" and self.command_exists(3):
            self.db.add_list(self.cmds[3:], target_date=self.cmds[1])
            return self.db.get(self.cmds[1])
        elif CommandValidator.is_date(self.cmds[1]) and CommandValidator.is_valid_index(self.cmds[2]) and not self.command_exists(3):
            return self.db.get_info(start_date=self.cmds[1], index=int(self.cmds[2]))
        elif CommandValidator.is_date(self.cmds[1]) and self.command_exists(2) and CommandValidator.is_date(self.cmds[2]):
            start_date, end_date = Helper.sortDates(self.cmds[1], self.cmds[2])
            return self.db.get_info(start_date=start_date, end_date=end_date)
        else:
            return "command not found"

    def greater_than_two_commands(self):
        if self.command_exists(2) and self.cmds[1] == "list":
            self.db.add_list(self.cmds[2:])
            return self.db.get_today_data()

        elif CommandValidator.is_duration(self.cmds[1]) and CommandValidator.is_valid_index(self.cmds[2]):
            self.db.add(self.cmds[1], index=int(self.cmds[2]))
            return self.db.get_today_data()

        elif self.cmds[1] == "pop" and CommandValidator.is_valid_index(self.cmds[2]):
            self.db.pop(int(self.cmds[2]))
            return self.db.get_today_data()

        else:
            return "command not found"

    def command_exists(self, index):
        return self.len_commands > index

    def setCommands(self, cmds: list):
        for i in range(len(cmds)):
            if cmds[i] == "today":
                cmds[i] = str(date.today())
        self._cmds = cmds

    @property
    def db(self):
        return self._db

    @property
    def len_commands(self):
        return len(self.cmds)

    @property
    def cmds(self):
        return self._cmds


class CommandExceptions(Exception):
    """raised when there is some problem command"""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class CommandNotFoundException(CommandExceptions):
    """raised when command not found"""

    def __init__(self, cmd: str):
        super().__init__(
            message=f"command_not_found: <{cmd}>: command not found")


class IncompleteCommandException(CommandExceptions):
    """raised when the command are correct but incomplete"""

    def __init__(self, cmd: str):
        message = f"incomplete_command: <{cmd}>: complete the command"
        super().__init__(message)
