from prompt_toolkit import prompt
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style
from Develops.DeepWork.database import dateDB
from commands import CommandValidator, CommandExecutor


class Terminal:
    def __init__(self):
        pass

    def setInput(self, input: str):
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


if __name__ == "__main__":
    import time
    T = Terminal()
    db = dateDB()
    cv = CommandValidator()
    executor = CommandExecutor(db)
    
    inputs = ["deepwork 0:30", "deepwork pop",
              "deepwork list 0:31 0:32 0:33",
              "deepwork today", "deepwork total","deepwork pop -10", "deepwork popall", 
              "deepwork 2025-04-18 list 0:30 0:31",
              "deepwork 2025-04-18 pop 1", "deepwork 2025-04-18",
              "deepwork 2025-04-18 1:00", "deepwork 2025-04-18 1:02 -10",
              "deepwork 2025-04-18 pop", "deepwork -10 2025-04-18 1:02",
              "deepwork 2025-04-18 popall", "deepwork 2025-04-18 list 0:30 0:31",]
    inputs = ["deepwork list 2025-04-18  0:30 0:31", "deepwork list 2025-04-18  0:30 0:31",
              ]
    while True:
        try:
            # inp = prompt(">>> ", lexer=Terminal.CommandLexer(),
            #              style=Terminal.style).strip()
            # if not inp:
            #     continue
            for inp in inputs:
                T.setInput(inp)
                out = ""
                print(T.cmds)
                if cv.validate(T.cmds):
                    print(executor.execute(T.cmds))
                    print("------------")
                time.sleep(8)
        except Exception as e:
            print(f"[Error] {e}")
