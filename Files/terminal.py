from prompt_toolkit import prompt
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style

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


