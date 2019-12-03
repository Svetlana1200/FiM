import sys
import enum
import os
import math

class BaseIO:
    def __init__(self):
        pass
    def print_line(self, line):
        pass
    @staticmethod
    def get_line(self):
        pass

class IO(BaseIO):
    def __init__(self):
        pass

    def print_line(self, line):
        print(line)

    def get_line(self):
        return input()


class IOTest(BaseIO):
    def __init__(self):
        self.value_print = ""
        self.value_get = ["cakes", "123"]

    def print_line(self, line):
        self.value_print += line  + "\n"

    def get_line(self):
        return self.value_get.pop()

class SymbolAndCommand(enum.Enum):
    (NUM, STRING, ID, PRINT, READ, ASK, APPROPRIATION,
     IF, ELSE, ENDIF, WHILE, ENDWHILE, PLUS, PLUSONE,
     MINUS, MINUSONE, DEVIDE, MULTIPLY,
     NOTEQ, EQUALS, LESS, MORE, EQLESS, EQMORE,
     PUNCTUATION, RPAR, LPAR, LBRA, RBRA, SEMICOLON,
     QUESTION, EXCLAMATION, DOT, TWOPOINTS,
     STARTCLASS, ENDCLASS, STARTMETHOD, ENDMETHOD, RETURN, CALLMETHOD,
     NAMEMETHOD, MAINMETHOD,
     TYPE) = range(43)


class Lexer:
    # специальные символы
    SYMBOLS = {'{': SymbolAndCommand.LBRA, '}': SymbolAndCommand.RBRA,
               ';': SymbolAndCommand.SEMICOLON, '(': SymbolAndCommand.LPAR,
               ')': SymbolAndCommand.RPAR, '?': SymbolAndCommand.QUESTION,
               '!': SymbolAndCommand.EXCLAMATION, '.': SymbolAndCommand.DOT,
               ':': SymbolAndCommand.TWOPOINTS}

    # ключевые слова
    WORDS = {
             'dear': SymbolAndCommand.STARTCLASS,
             'your faithful student,': SymbolAndCommand.ENDCLASS,
             'today i learned': SymbolAndCommand.MAINMETHOD,
             'i learned': SymbolAndCommand.STARTMETHOD,
             'then you get': SymbolAndCommand.RETURN,
             "that's all about": SymbolAndCommand.ENDMETHOD,
             'i remembered': SymbolAndCommand.CALLMETHOD,

             'did you know that': SymbolAndCommand.APPROPRIATION,
             'is now': SymbolAndCommand.APPROPRIATION,
             'now': SymbolAndCommand.APPROPRIATION,
             'are now': SymbolAndCommand.APPROPRIATION,
             'now like': SymbolAndCommand.APPROPRIATION,
             'now become': SymbolAndCommand.APPROPRIATION,

             'as long as': SymbolAndCommand.WHILE,
             "here's what I did while": SymbolAndCommand.WHILE,
             "that's what i did": SymbolAndCommand.ENDWHILE,

             'if': SymbolAndCommand.IF, 'when': SymbolAndCommand.IF,
             'otherwise': SymbolAndCommand.ELSE,
             'or else': SymbolAndCommand.ELSE,
             "that's what i would do": SymbolAndCommand.ENDIF,

             'less than': SymbolAndCommand.LESS,
             'more than': SymbolAndCommand.MORE,
             'greater than': SymbolAndCommand.MORE,
             'no more than': SymbolAndCommand.EQLESS,
             'not more': SymbolAndCommand.EQLESS,
             'no greater than': SymbolAndCommand.EQLESS,
             'not greater': SymbolAndCommand.EQLESS,
             'no less than': SymbolAndCommand.EQMORE,
             'not less': SymbolAndCommand.EQMORE,

             'is': SymbolAndCommand.EQUALS, 'was': SymbolAndCommand.EQUALS,
             'has': SymbolAndCommand.EQUALS, 'had': SymbolAndCommand.EQUALS,
             'not': SymbolAndCommand.NOTEQ,

             "i said": SymbolAndCommand.PRINT,
             'i wrote': SymbolAndCommand.PRINT,
             'i sang': SymbolAndCommand.PRINT,
             'i thought': SymbolAndCommand.PRINT,
             'i heard': SymbolAndCommand.READ, 'i read': SymbolAndCommand.READ,
             'i asked': SymbolAndCommand.ASK,

             'i would add': SymbolAndCommand.PLUS,
             #"add": SymbolAndCommand.PLUS,
             "plus": SymbolAndCommand.PLUS,
             "added to": SymbolAndCommand.PLUS,
             #"got one more": SymbolAndCommand.PLUSONE,
             'i would subtract': SymbolAndCommand.MINUS,
             #'subtract': SymbolAndCommand.MINUS,
             #"the difference between": SymbolAndCommand.MINUS,
             #"got one less": SymbolAndCommand.MINUSONE,
             'minus': SymbolAndCommand.MINUS,
             "without": SymbolAndCommand.MINUS,
             'i would multiply': SymbolAndCommand.MULTIPLY,
             'times': SymbolAndCommand.MULTIPLY,
             'multiplied with': SymbolAndCommand.MULTIPLY,
             #'multiply': SymbolAndCommand.MULTIPLY,
             'i would divide':  SymbolAndCommand.DEVIDE,
             'divided by': SymbolAndCommand.DEVIDE,
             #'divide': SymbolAndCommand.DEVIDE,

             'the number': SymbolAndCommand.NUM,
             'the word': SymbolAndCommand.STRING
             }

    def __init__(self, text):
        self.text = text
        self.index = 0
        self.has_command = False
        self.ch = None
        self.getc()

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
        return self.value.rstrip(), self.sym

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
        self.sym = SymbolAndCommand.STRING

    def get_punctuation(self):
        self.has_command = False
        while self.ch in Lexer.SYMBOLS:
            self.get_next_symbol()
        self.sym = SymbolAndCommand.PUNCTUATION

    def get_arguments(self):
        while ((self.ch.isalpha() or self.ch.isspace()
                or self.ch.isdigit() or self.ch == "'"
                or self.ch == "*" or self.ch == "-" or self.ch == "+")
                and self.sym is None):
            self.get_next_symbol()
        self.sym = SymbolAndCommand.ID

    def get_next_symbol(self, replace_to_lower=False):
        if replace_to_lower:
            self.value += self.ch.lower()
        else:
            self.value += self.ch
        self.getc()


class Interpretator:
    def __init__(self, text, io=IO()):
        lexer = Lexer(text)
        self.tokens = []
        while lexer.index <= len(lexer.text):
            next_tok = lexer.next_tok()
            self.tokens.append(next_tok)
            # print(next_tok)

        self.in_method = False
        self.in_what_method = []
        self.is_exectute_if = False
        self.method = {}
        self.classes = {}
        self.variables = {}
        self.circle = []  # имя переменной, больше/меньше, величина
        self.circle_ind = None
        self.io = io
        self.ind = 0

    def approptiate_value(self):
        ind_start = self.ind
        should_ignore = [
            " was ", " is ", " has ",
            " had ", " like ", " likes ", " liked "
            ]
        for word in should_ignore:
            if self.tokens[self.ind+1][0].find(word) != -1:
                variable, value = self.tokens[self.ind + 1][0].split(word)
                if variable in self.variables:
                    if (self.variables[variable][0] == SymbolAndCommand.NUM
                            and value.isdigit()):
                        self.approptiate_nuber(value, variable)
                    elif value in self.variables:
                        self.approptiate_value_variable(value, variable)
                    elif value in self.method or value.find(" using ") != -1:
                        has_args = False
                        if value.find(" using ") != -1:
                            has_args = True
                        value = self.approptiate_value_method(
                            value, variable, has_args)
                        self.ind = self.method[value]['start_ind']
                    else:
                        self.approptiate_value_operation(value, variable)
                else:
                    self.init_variable(variable, value)
                break
        if ind_start == self.ind:
            self.ind += 2
        # print("did you know", self.variables)

    def init_variable(self, variable, value):
        should_find_type = ["the number", "the word"]
        for types in should_find_type:
            if value.find(types) != -1:
                this_type = Lexer.WORDS[types]
                value = value[
                    value.find(types) + len(types) + 1:]
                if (this_type == SymbolAndCommand.NUM and
                        value.rstrip() != ""):
                    value = int(value)
                self.variables[variable] = [
                    this_type, value]
                break

    def approptiate_value_operation(self, value, variable):
        operations = [
                    " plus ", " added to ", ' minus ',
                    " without ", ' times ', ' multiplied with ',
                    ' divided by ']
        this_operation = None
        for operation in operations:
            if value.find(operation) != -1:
                this_operation = Lexer.WORDS[operation[1:-1]]
                first, second = value.split(operation)
                first, _was_conver = self.try_conver_to_int(first)
                second, _was_conver = self.try_conver_to_int(second)
                break
        if this_operation is None:
            self.variables[variable][1] = value
        elif this_operation == SymbolAndCommand.MINUS:
            self.variables[variable][1] = first - second
        elif this_operation == SymbolAndCommand.MULTIPLY:
            self.variables[variable][1] = first * second
        elif this_operation == SymbolAndCommand.PLUS:
            self.variables[variable][1] = first + second
        elif this_operation == SymbolAndCommand.DEVIDE:
            self.variables[variable][1] = math.floor(first / second)

    def approptiate_value_variable(self, value, variable):
        self.variables[variable][1] = self.variables[value][1]

    def approptiate_nuber(self, value, variable):
        self.variables[variable][1] = int(value)

    def approptiate_value_method(self, value, variable, has_args):
        if has_args:
            value, args = value.split(" using ")
            args = args.split(' and ')
            for i in range(len(self.method[value]['using_values'])):
                self.variables[
                    self.method[value]['using_values'][i]
                    ] = self.variables[args[i]]
        self.method[value]['result'] = variable
        self.method[value]['save_ind'] = self.ind + 2
        self.in_what_method.append(value)
        return value

    def print_line(self, command, type_command):
        text = ""
        self.ind += 1
        command, type_command = self.tokens[self.ind]
        while type_command != SymbolAndCommand.PUNCTUATION:
            if (type_command == SymbolAndCommand.STRING or
                    type_command == SymbolAndCommand.NUM or
                    command not in self.variables):
                text += command
            else:
                text += str(self.variables[command][1])
            self.ind += 1
            command, type_command = self.tokens[self.ind]
        self.io.print_line(text)

    def read_line(self, variable=None):
        if variable is None:
            variable = self.tokens[self.ind + 1][0]
        value = self.io.get_line()
        if self.variables[variable][0] == SymbolAndCommand.STRING:
            self.variables[variable][1] = value
        elif self.variables[variable][0] == SymbolAndCommand.NUM:
            self.variables[variable][1] = int(value)
        self.ind += 2

    def ask_line(self):
        self.io.print_line(self.tokens[self.ind + 2][0])
        self.read_line(self.tokens[self.ind + 1][0])
        self.ind += 1

    def make_arithmetic(self, should_replace, operation):
        values = self.tokens[self.ind + 1][0]
        for word in should_replace:
            if values.find(word) != -1:
                res_replace = values.replace(word, ".")
                first, second = res_replace.split(".")
                if operation == SymbolAndCommand.DEVIDE:
                    first, second = second, first
                first_value, _was_conver = self.try_conver_to_int(first, first)
        if operation == SymbolAndCommand.PLUS:
            self.variables[second][1] += first_value
        elif operation == SymbolAndCommand.MINUS:
            self.variables[second][1] -= first_value
        elif operation == SymbolAndCommand.MULTIPLY:
            self.variables[second][1] *= first_value
        elif operation == SymbolAndCommand.DEVIDE:
            self.variables[second][1] = math.floor(
                self.variables[second][1] / first_value)
        self.ind += 2

    def start_while(self):
        string = self.tokens[self.ind + 1][0]
        should_replace = [
            " was ", " is ", " has ",
            " had ", " like ", " likes ", " liked "]
        for word in should_replace:
            if string.find(word) != -1:
                ind_find = string.find(word)
                name = string[: ind_find]
                value = string[ind_find + len(word):]
                string = string.replace(word, " ")
                break
        should_find = [
            " no more than ", ' no less than ',
            ' no greater than ',
            ' not more ', ' not greater ', ' not less ',
            ' less than ', ' more than ', ' greater than ',
            " not "
            ]
        find_operation = False
        for eq in should_find:
            ind_find = string.find(eq)
            if ind_find != -1:
                find_operation = True
                name = string[: ind_find]
                self.circle.append(name)
                self.circle.append(Lexer.WORDS[eq[1:-1]])
                value = string[ind_find + len(eq):]
                if value.isdigit():
                    self.circle.append(int(value))
                else:
                    self.circle.append(self.variables[value][1])
                break
        if not find_operation:
            self.circle.append(name)
            self.circle.append(SymbolAndCommand.EQUALS)
            if value.isdigit():
                self.circle.append(int(value))
            else:
                self.circle.append(self.variables[value][1])
        self.circle_ind = self.ind + 2
        self.ind += 2

    def check_ending_while(self):
        if (self.circle[1] == SymbolAndCommand.MORE and
                self.variables[self.circle[0]][1] <= self.circle[2] or
                self.circle[1] == SymbolAndCommand.LESS and
                self.variables[self.circle[0]][1] >= self.circle[2] or
                self.circle[1] == SymbolAndCommand.EQLESS and
                self.variables[self.circle[0]][1] > self.circle[2] or
                self.circle[1] == SymbolAndCommand.EQMORE and
                self.variables[self.circle[0]][1] < self.circle[2] or
                self.circle[1] == SymbolAndCommand.NOTEQ and
                self.variables[self.circle[0]][1] == self.circle[2] or
                self.circle[1] == SymbolAndCommand.EQUALS and
                self.variables[self.circle[0]][1] != self.circle[2]):
            self.ind += 1
            # print("finish while")
        else:
            self.ind = self.circle_ind

    def start_if(self):
        condition = self.tokens[self.ind + 1][0]
        should_replace = [" was ", " is ", " has ", " had "]
        for word in should_replace:
            if condition.find(word) != -1:
                first, second = condition.split(word)
                second = second.replace(" then", "")
                first, _was_convert = self.try_conver_to_int(first)
                second, _was_convert = self.try_conver_to_int(second)
                condition = condition.replace(word, " ")
                break
        comparators = [
            ' no less than ', ' no more than ', ' no greater than ',
            ' not more ', ' not greater ', ' not less ',
            ' more than ', ' greater than ', ' less than ', ' not ',
            ]
        operation = None

        for e in comparators:
            if condition.find(e) != -1:
                operation = Lexer.WORDS[e[1:-1]]
                condition = condition.replace(" then", "")
                parts = condition.split(e)
                first, _was_convert = self.try_conver_to_int(first, parts[0])
                second, _was_oinvert = self.try_conver_to_int(second, parts[1])
                break
        if operation is None:
            operation = SymbolAndCommand.EQUALS
        if Interpretator.check_if_condition(operation, first, second):
            self.ind += 2
            self.is_exectute_if = True
        else:
            self.ind += 2
            type_command = self.tokens[self.ind][1]

            while (type_command != SymbolAndCommand.ELSE
                    and type_command != SymbolAndCommand.ENDIF):
                self.ind += 1
                type_command = self.tokens[self.ind][1]

    def start_method(self):
        self.method_with_name_return_args = (
            self.tokens[self.ind + 1][0].replace('about ', ""))
        name = None
        return_type = None
        using_values = None
        if self.method_with_name_return_args.find(' with ') != -1:
            name, self.method_with_return_args = (
                self.method_with_name_return_args.split(' with '))
            if self.method_with_return_args.find(' using ') != -1:
                return_type, args = (
                    self.method_with_return_args.split(' using '))
                using_values = args.split(" and ")
            else:
                return_type = self.method_with_return_args
        elif self.method_with_name_return_args.find(' using ') != -1:
            name, args = (
                self.method_with_name_return_args.split(' using '))
            using_values = args.split(" and ")
        self.method[name] = {
            'is_main': False,
            'start_ind': self.ind + 3,
            'return_type': return_type,
            'using_values': using_values,
        }
        self.in_method = True
        self.ind += 2

    def keep_info_main_method(self):
        name = self.tokens[self.ind+1][0].replace('about ', "")
        self.method[name] = {
            'is_main': True,
            'start_ind': self.ind + 3,
            'return_type': None,
            'using_values': None,
        }
        self.ind += 2

    def end_method(self):
        name = self.tokens[self.ind + 1][0]
        if len(self.method[name]) == 4:
            self.in_method = False
            self.method[name]['finish_ind'] = self.ind
            self.ind += 2
        else:
            self.ind = self.method[name]['save_ind']
            self.method[name].pop('save_ind')

    def call_method(self):
        name_method_with_args = self.tokens[self.ind + 1][0]
        if name_method_with_args.find(" using ") != -1:
            name_method, args = name_method_with_args.split(" using ")
            args = args.split(', ')
            for i in range(len(self.method[name_method]['using_values'])):
                if args[i] in self.variables:
                    self.variables[
                        self.method[name_method]['using_values'][i]
                        ] = self.variables[args[i]]
                elif args[i].isdigit():
                    self.variables[
                        self.method[name_method]['using_values'][i]
                        ] = [SymbolAndCommand.NUM, int(args[i])]
        else:
            name_method = name_method_with_args
        self.method[name_method]['save_ind'] = self.ind + 2
        self.ind = self.method[name_method]['start_ind']
        self.in_what_method.append(name_method)

    def return_value_from_method(self):
        answer = self.tokens[self.ind + 1][0]
        answer, _was_conver = self.try_conver_to_int(answer)
        self.ind += 2
        name_method = self.in_what_method.pop()
        name_value = self.method[name_method]['result']
        self.method[name_method].pop('result')

        self.variables[name_value][1] = answer

    def start_class(self):
        tmp = []
        self.ind += 1
        command, type_command = self.tokens[self.ind]
        while type_command != SymbolAndCommand.PUNCTUATION:
            tmp.append(command)
            self.ind += 1
            command, type_command = self.tokens[self.ind]
        tmp.append(self.ind + 3)
        self.classes[self.tokens[self.ind + 1][0]] = tmp
        self.ind += 3

    def end_class(self):
        for name_class in self.classes.keys():
            value = self.classes[name_class][-2]
            if not self.try_conver_to_int(value)[1]:
                self.classes[name_class].append(self.ind)
        self.ind += 2

    @staticmethod
    def check_if_condition(operation, first, second):
        return (operation == SymbolAndCommand.MORE and
                first > second or
                operation == SymbolAndCommand.LESS and
                first < second or
                operation == SymbolAndCommand.EQLESS and
                first <= second or
                operation == SymbolAndCommand.EQMORE and
                first >= second or
                operation == SymbolAndCommand.EQUALS and
                first == second or
                operation == SymbolAndCommand.NOTEQ and
                first != second)

    def try_conver_to_int(self, value1, value2=None):
        if value2 is None:
            value2 = value1
        try:
            value1 = int(value2)
            return value1, True
        except ValueError:
            if value2 in self.variables:
                value1 = self.variables[value2][1]
                return value1, True
        return value1, False

    def execute(self):
        while self.ind < len(self.tokens):
            command, type_command = self.tokens[self.ind]
            if (self.in_method and
                    type_command != SymbolAndCommand.ENDMETHOD):
                self.ind += 1
                continue

            elif type_command == SymbolAndCommand.APPROPRIATION:
                self.approptiate_value()
            elif type_command == SymbolAndCommand.PUNCTUATION:
                self.ind += 1

            elif type_command == SymbolAndCommand.PRINT:
                self.print_line(command, type_command)
            elif type_command == SymbolAndCommand.READ:
                self.read_line()
            elif type_command == SymbolAndCommand.ASK:
                self.ask_line()

            elif (type_command == SymbolAndCommand.PLUS
                    or type_command == SymbolAndCommand.MINUS
                    or type_command == SymbolAndCommand.MULTIPLY
                    or type_command == SymbolAndCommand.DEVIDE):
                if type_command == SymbolAndCommand.PLUS:
                    should_replace = [" to ", " and "]
                elif type_command == SymbolAndCommand.MINUS:
                    should_replace = [" from ", " and "]
                elif type_command == SymbolAndCommand.MULTIPLY:
                    should_replace = [" and "]
                else:
                    should_replace = [" by ", " and "]
                self.make_arithmetic(should_replace, type_command)

            elif type_command == SymbolAndCommand.WHILE:
                self.start_while()
            elif type_command == SymbolAndCommand.ENDWHILE:
                self.check_ending_while()

            elif type_command == SymbolAndCommand.STARTMETHOD:
                self.start_method()
            elif type_command == SymbolAndCommand.MAINMETHOD:
                self.keep_info_main_method()
            elif type_command == SymbolAndCommand.ENDMETHOD:
                self.end_method()
            elif type_command == SymbolAndCommand.CALLMETHOD:
                self.call_method()
            elif type_command == SymbolAndCommand.RETURN:
                self.return_value_from_method()

            elif type_command == SymbolAndCommand.STARTCLASS:
                self.start_class()
            elif type_command == SymbolAndCommand.ENDCLASS:
                self.end_class()

            elif type_command == SymbolAndCommand.IF:
                self.start_if()
            elif type_command == SymbolAndCommand.ENDIF:
                self.ind += 1
                self.is_exectute_if = False
            elif type_command == SymbolAndCommand.ELSE:
                if self.is_exectute_if:
                    while self.tokens[self.ind][1] != SymbolAndCommand.ENDIF:
                        self.ind += 1
                self.ind += 1
                self.is_exectute_if = False
            else:
                print("Wrong token: " + self.tokens[self.ind][0])


def main():
    if len(sys.argv) == 2:
        name_file = sys.argv[1]
        if os.path.exists(name_file):
            with open(name_file, 'r') as f:
                text = f.read().rstrip()
        else:
            print("Не удается найти указанный файл.")
            exit()
    else:
        text = sys.stdin.read().rstrip()
        if text == "":
            exit()

    i = Interpretator(text, IO())
    i.execute()

    # print(i.variables)
    # print(i.method)
    # print(i.classes)


if __name__ == "__main__":
    main()
