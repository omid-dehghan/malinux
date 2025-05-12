from datetime import datetime, date
from Develops.Deepwork.duration import DurationList
from Develops.Deepwork.database import Database
from Develops.Deepwork.database import DataStorage
from Develops.Deepwork.analyzer import DataAnalyzer
from Develops.Deepwork.chart import Chart
from Develops.Deepwork.database import Helper
from Develops.Deepwork.config import Config


class CommandValidator:
    MAIN_COMMANDS = ["deepwork",
                     "pop",
                     "popall",
                     "list",
                     "today",
                     "total",
                     "barchart",
                     "set",
                     "filename",
                     "path",
                     "alldata",
                     "clear",
                     "get",
                     "filepath"
                     ]

    def __init__(self):
        pass

    def validate(self, cmds):
        if cmds[1] == "set" and (cmds[2] == "filename" or cmds[2] == "path"):
            self._cmds = cmds
            return True
        else:
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

    def __init__(self, db: Database, da: DataAnalyzer, config: Config, ds: DataStorage, ch: Chart
                 ):
        self._db = db
        self._da = da
        self._ch = ch
        self._config = config
        self._ds = ds

    def execute(self, cmds):
        self.setCommands(cmds)
        if self.cmds[0] == "deepwork":
            if self.command_exists(1) and (self.cmds[1].lower() == "set" or self.cmds[1].lower() == "get"):
                return self.config_related_commands()
            elif self.command_exists(1) and CommandValidator.is_date(self.cmds[1]):
                return self.date_related_commands()
            elif self.len_commands > 2:
                return self.greater_than_two_commands()
            elif len(self.cmds) == 2:
                return self.two_layer_commands()
            else:
                return "command not found"
        else:
            return f"command_not_found: <{self.cmds[0]}>: command not found"

    def one_layer_command(self):
        if self.cmds[0] == "deepwork":
            raise IncompleteCommandException(self.cmds[0])

    def config_related_commands(self):
        if self.command_exists(1) and self.cmds[1] == "set" and self.command_exists(2):
            if self.cmds[2] == "path" and self.command_exists(3):
                return self.config.set("path", self.cmds[3])
            elif self.cmds[2] == "filename" and self.command_exists(3):
                message = self.config.set("filename", self.cmds[3])
                self.ds.setPath(self.config.get_filepath())
                self.db.reload()
                return message
        elif self.command_exists(1) and self.cmds[1] == "get" and self.command_exists(2) and self.cmds[2] == "filepath" and not self.command_exists(3):
            return self.config.get_filepath()
        else:
            return "command not found"

    def two_layer_commands(self):
        # pop commands
        cmd = self.cmds[1]
        if cmd == "pop":
            return self.db.perform_action(cmd)
        elif cmd == "popall":
            return self.db.perform_action(cmd)
        elif cmd == "today":
            return self.db.get_today_data()
        elif cmd == "alldata":
            return self.db.perform_action(cmd)
        elif CommandValidator.is_duration(cmd):
            return self.db.perform_action("add", duration=cmd)
        # Analyzes
        elif cmd == "total":
            return self.da.get_info()
        elif CommandValidator.is_valid_index(self.cmds[1]):
            return self.da.get_info(int(self.cmds[1]))
        elif cmd == "barchart":
            self.ch.bar_chart()
        else:
            return f"command_not_found: <{self.cmds[1]}>: command not found"

    def date_related_commands(self):
        # get data
        if CommandValidator.is_date(self.cmds[1]) and not self.command_exists(2):
            return self.db.perform_action("get", target_date=self.cmds[1])
        # single duration append
        elif CommandValidator.is_date(self.cmds[1]) and CommandValidator.is_duration(self.cmds[2]) and not self.command_exists(3):
            return self.db.perform_action("add",
                                          target_date=self.cmds[1], duration=self.cmds[2])
        # single duration insert
        elif CommandValidator.is_date(self.cmds[1]) and CommandValidator.is_duration(self.cmds[2]) and CommandValidator.is_valid_index(self.cmds[3]):
            return self.db.perform_action("add",
                                          target_date=self.cmds[1], duration=self.cmds[2], index=int(self.cmds[3]))
        # single duration pop
        elif CommandValidator.is_date(self.cmds[1]) and self.cmds[2] == "pop" and not self.command_exists(3):
            return self.db.perform_action("pop", target_date=self.cmds[1])
        # single pop indexed
        elif CommandValidator.is_date(self.cmds[1]) and self.cmds[2] == "pop" and CommandValidator.is_valid_index(self.cmds[3]):
            return self.db.perform_action("pop",
                                          target_date=self.cmds[1], index=int(self.cmds[3]))
        # pop all
        elif CommandValidator.is_date(self.cmds[1]) and self.cmds[2] == "popall":
            return self.db.perform_action("popall", target_date=self.cmds[1])
        # list append
        elif CommandValidator.is_date(self.cmds[1]) and self.cmds[2] == "list" and self.command_exists(3):
            return self.db.perform_action("addlist", durations=self.cmds[3:], target_date=self.cmds[1])
        elif CommandValidator.is_date(self.cmds[1]) and CommandValidator.is_valid_index(self.cmds[2]) and not self.command_exists(3):
            return self.da.get_info(start_date=self.cmds[1], index=int(self.cmds[2]))
        elif CommandValidator.is_date(self.cmds[1]) and self.command_exists(2) and CommandValidator.is_date(self.cmds[2]):
            start_date, end_date = Helper.sortDates(self.cmds[1], self.cmds[2])
            return self.da.get_info(start_date=start_date, end_date=end_date)
        else:
            return "command not found"

    def greater_than_two_commands(self):
        if self.command_exists(2) and self.cmds[1] == "list":
            return self.db.perform_action("addlist", durations=self.cmds[2:])

        elif CommandValidator.is_duration(self.cmds[1]) and CommandValidator.is_valid_index(self.cmds[2]):
            return self.db.perform_action("add", duration=self.cmds[1], index=int(self.cmds[2]))

        elif self.cmds[1] == "pop" and CommandValidator.is_valid_index(self.cmds[2]):
            return self.db.perform_action("pop", index=int(self.cmds[2]))

        elif self.cmds[1] == "clear" and self.cmds[2] == "alldata":
            while True:
                inp = input("Are you sure? [Y/N]")
                if inp.lower() == "y":
                    return self.db.perform_action("clearalldata")
                else:
                    break
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
    def da(self):
        return self._da

    @property
    def ch(self):
        return self._ch

    @property
    def ds(self):
        return self._ds

    @property
    def config(self):
        return self._config

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
