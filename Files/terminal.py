from turtle import textinput
from prompt_toolkit import prompt
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style
from Develops.DeepWork.database import dateDB
import re



class Terminal:
    def __init__(self):
        pass

    def setInput(self, input:str):
        self._input = input

    @property
    def input(self):
        return self._input
    
    @property
    def cmds(self):
        if self.input == None:
            return None
        elif self.input == " ":
            return None
        else:
            return self.input.split()
        
    # Define your color rules here
    highlight_words = {
        "deepwork": "class:deepwork",

    }

    # Define your color styles
    style = Style.from_dict({
        "deepwork": "ansiyellow",
    })

    # Custom lexer that applies colors as the user types
    class CommandLexer(Lexer):
        def lex_document(self, document):
            text = document.text

            def get_tokens(pos):
                result = []
                words = text.split(" ")
                current_pos = 0
                for word in words:
                    word_len = len(word)
                    style = Terminal.highlight_words.get(word, "")
                    result.extend([(style, c) for c in word])
                    result.append(("", " "))  # Add back the space
                    current_pos += word_len + 1
                return result
            return get_tokens

    def check_inp(self):
        db = dateDB()
        # layer 0
        if self.cmds[0] == "deepwork":
            # layer 1
            if not self.command_exists(1):
                return "command_not_found"
            cmd = self.cmds[1].lower()
            # pop commands
            if cmd == "pop":
                db.pop()
                return db.get_today_data()
            elif cmd == "popall":
                db.pop_all()
                return db.get_today_data()
            # add commands
            elif re.match(r"^\d{1,2}:\d{2}$", cmd):
                if self.command_exists(2):
                    db.add(cmd, index=int(self.cmds[2]))
                elif not self.command_exists(2):
                    db.add(cmd)
                return db.get_today_data()
            elif cmd == "list":
                db.add_list(self.cmds[2:])
                return db.get_today_data()
            
            # find commands
            elif cmd == "today":
                return db.get_today_data()
            elif re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", cmd):
                return db.get(cmd)
            else:
                return f"command_not_found: <{cmd}>: command not found"
        else:
            return f"command_not_found: <{self.input}>: command not found"

    def command_exists(self, index):
        return len(self.cmds) > index
    

if __name__ == "__main__":
    T = Terminal()
    while True:
        try:
            inp = prompt(">>> ", lexer=Terminal.CommandLexer(),
                         style=Terminal.style).strip()
            if not inp:
                continue
            T.setInput(inp)
            out = T.check_inp()
            print(out)
        except Exception as e:
            print(f"[Error] {e}")
