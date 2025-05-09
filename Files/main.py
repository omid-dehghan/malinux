from prompt_toolkit import prompt
from Develops.DeepWork.database import Database, DataStorage
from Develops.DeepWork.analyzer import DataAnalyzer
from Develops.DeepWork.chart import Chart
from commands import CommandValidator, CommandExecutor
from terminal import Terminal
import threading
import os

class DeepWorkApp:
    def __init__(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "deepwork.json")

        # Initialize components
        self.T = Terminal()
        self.ds = DataStorage(file_path)
        self.db = Database(self.ds)
        self.da = DataAnalyzer(self.db)
        self.cv = CommandValidator()
        self.ch = Chart(self.db)
        self.executor = CommandExecutor(self.db, self.da, self.ch)

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
        # Start the CLI in a background thread
        threading.Thread(target=self.run_cli, daemon=True).start()

        # Run the chart in the main thread
        self.ch.bar_chart()

if __name__ == "__main__":
    app = DeepWorkApp()
    app.start()
