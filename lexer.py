from symbolAndCommand import TOKEN_TYPES
import sys


class Token:
    def __init__(self, command, type_command):
        self.command = command
        self.type_command = type_command


class Lexer:
    # специальные символы
    SYMBOLS = {'{': TOKEN_TYPES.LBRA, '}': TOKEN_TYPES.RBRA,
               ';': TOKEN_TYPES.SEMICOLON, '(': TOKEN_TYPES.LPAR,
               ')': TOKEN_TYPES.RPAR, '?': TOKEN_TYPES.QUESTION,
               '!': TOKEN_TYPES.EXCLAMATION, '.': TOKEN_TYPES.DOT,
               ':': TOKEN_TYPES.TWOPOINTS}

    # ключевые слова
    WORDS = {
             'dear': TOKEN_TYPES.STARTCLASS,
             'your faithful student,': TOKEN_TYPES.ENDCLASS,
             'today i learned': TOKEN_TYPES.MAINMETHOD,
             'i learned': TOKEN_TYPES.STARTMETHOD,
             'then you get': TOKEN_TYPES.RETURN,
             "that's all about": TOKEN_TYPES.ENDMETHOD,
             'i remembered': TOKEN_TYPES.CALLMETHOD,

             'did you know that': TOKEN_TYPES.APPROPRIATION,
             'is now': TOKEN_TYPES.APPROPRIATION,
             'now': TOKEN_TYPES.APPROPRIATION,
             'are now': TOKEN_TYPES.APPROPRIATION,
             'now like': TOKEN_TYPES.APPROPRIATION,
             'now become': TOKEN_TYPES.APPROPRIATION,

             'as long as': TOKEN_TYPES.WHILE,
             "here's what I did while": TOKEN_TYPES.WHILE,
             "that's what i did": TOKEN_TYPES.ENDWHILE,

             'if': TOKEN_TYPES.IF, 'when': TOKEN_TYPES.IF,
             'otherwise': TOKEN_TYPES.ELSE,
             'or else': TOKEN_TYPES.ELSE,
             "that's what i would do": TOKEN_TYPES.ENDIF,

             'less than': TOKEN_TYPES.LESS,
             'more than': TOKEN_TYPES.MORE,
             'greater than': TOKEN_TYPES.MORE,
             'no more than': TOKEN_TYPES.EQLESS,
             'not more': TOKEN_TYPES.EQLESS,
             'no greater than': TOKEN_TYPES.EQLESS,
             'not greater': TOKEN_TYPES.EQLESS,
             'no less than': TOKEN_TYPES.EQMORE,
             'not less': TOKEN_TYPES.EQMORE,

             'is': TOKEN_TYPES.EQUALS, 'was': TOKEN_TYPES.EQUALS,
             'has': TOKEN_TYPES.EQUALS, 'had': TOKEN_TYPES.EQUALS,
             'not': TOKEN_TYPES.NOTEQ,

             "i said": TOKEN_TYPES.PRINT,
             'i wrote': TOKEN_TYPES.PRINT,
             'i sang': TOKEN_TYPES.PRINT,
             'i thought': TOKEN_TYPES.PRINT,
             'i heard': TOKEN_TYPES.READ, 'i read': TOKEN_TYPES.READ,
             'i asked': TOKEN_TYPES.ASK,

             'i would add': TOKEN_TYPES.PLUS,
             "plus": TOKEN_TYPES.PLUS,
             "added to": TOKEN_TYPES.PLUS,
             'i would subtract': TOKEN_TYPES.MINUS,
             'minus': TOKEN_TYPES.MINUS,
             "without": TOKEN_TYPES.MINUS,
             'i would multiply': TOKEN_TYPES.MULTIPLY,
             'times': TOKEN_TYPES.MULTIPLY,
             'multiplied with': TOKEN_TYPES.MULTIPLY,
             'i would divide':  TOKEN_TYPES.DIVIDE,
             'divided by': TOKEN_TYPES.DIVIDE,

             'the number': TOKEN_TYPES.NUM,
             'the word': TOKEN_TYPES.STRING
             }

    def __init__(self, text):
        self.text = text
        self.index = 0
        self.has_command = False
        self.ch = None
        self.getc()
        self.was_ok = ""

    def __iter__(self):
            return self

    def __next__(self):
        if self.index <= len(self.text):
            return self.next_tok()
        else:
            raise StopIteration

    def getc(self):
        try:
            self.ch = self.text[self.index]
        except Exception:
            self.ch = None
        finally:
            self.index += 1

    def next_tok(self):
        self.value = ""
        self.sym = None
        ind = self.index
        while self.ch.isspace():
            self.getc()
        if self.ch.isalpha() and not self.has_command:
            self.get_command()
        elif self.ch.isalpha() or self.ch.isspace() or self.ch.isdigit():
            self.get_arguments()
        elif self.ch == "\"":
            self.get_str_in_quater()
        elif self.ch in Lexer.SYMBOLS:
            self.get_punctuation()
        if ind == self.index:
            end_ind = self.text[ind:].find('\n') + ind
            start_ind = self.text[:ind].rfind('\n')
            print("Wrong string: ", self.text[start_ind:end_ind])
            sys.exit(1)
            
        return Token(self.value.rstrip(), self.sym)

    def get_command(self):
        while ((self.ch.isalpha() or self.ch == "'" or
                self.ch == "," or self.ch.isspace() or
                self.ch == "'") and self.sym is None):
            if self.value in Lexer.WORDS:
                self.sym = Lexer.WORDS[self.value]
                break
            self.get_next_symbol(True)
        if self.value in Lexer.WORDS:
            self.sym = Lexer.WORDS[self.value]
        self.has_command = True

    def get_str_in_quater(self):
        self.getc()
        while (self.ch != "\"") and self.sym is None and self.ch is not None:
            self.get_next_symbol()
        self.getc()
        self.sym = TOKEN_TYPES.STRING

    def get_punctuation(self):
        self.has_command = False
        while self.ch in Lexer.SYMBOLS:
            self.get_next_symbol()
        self.sym = TOKEN_TYPES.PUNCTUATION

    def get_arguments(self):
        while ((self.ch.isalpha() or self.ch.isspace()
                or self.ch.isdigit() or self.ch == "'"
                or self.ch == "*" or self.ch == "-" or self.ch == "+")
                and self.sym is None):
            self.get_next_symbol()
        self.sym = TOKEN_TYPES.ID

    def get_next_symbol(self, replace_to_lower=False):
        if replace_to_lower:
            self.value += self.ch.lower()
        else:
            self.value += self.ch
        self.getc()
