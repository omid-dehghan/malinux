from prompt_toolkit import prompt
from Develops.Deepwork.database import Database, DataStorage
from Develops.Deepwork.analyzer import DataAnalyzer
from Develops.Deepwork.chart import Chart
from Develops.Deepwork.config import Config
from commands import CommandValidator, CommandExecutor
from terminal import Terminal
import threading


class DeepWorkApp:
    def __init__(self):
        self.config = Config(r"Files\Develops\Deepwork\config.json")
        file_path = f"{self.config.get('filepath', 'C:/Users/Green/Desktop')}{self.config.get('filename', '/deepwork')}.json"
        # Initialize components
        self.T = Terminal()
        self.ds = DataStorage(file_path)
        self.db = Database(self.ds)
        self.da = DataAnalyzer(self.db)
        self.cv = CommandValidator()
        self.ch = Chart(self.db)
        self.executor = CommandExecutor(self.db, self.da, self.ch, self.config)

    def run_cli(self):
        """Runs the command-line interface in a background thread."""
        while True:
            try:
                inp = prompt(">>> ", lexer=Terminal.CommandLexer(),
                             style=Terminal.style).strip()
                if not inp:
                    continue
                self.T.setInput(inp)
                if self.cv.validate(self.T.cmds):
                    print(self.executor.execute(self.T.cmds))
            except Exception as e:
                print(f"[Error] {e}")

    def start(self):
        threading.Thread(target=self.run_cli, daemon=True).start()
        self.ch.bar_chart()


if __name__ == "__main__":
    app = DeepWorkApp()
    app.start()
