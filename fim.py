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
        self.value = None
        self.sym = None
        while self.ch.isspace():
            self.getc()
        if self.ch.isalpha() and not self.has_command:  # команда
            ident = ''
            while ((self.ch.isalpha() or self.ch == "'" or
                   self.ch == "," or self.ch.isspace() or
                   self.ch == "'") and self.sym is None):
                if ident in Lexer.WORDS:
                    self.sym = Lexer.WORDS[ident]
                    break
                ident = ident + self.ch.lower()
                self.getc()
            if ident in Lexer.WORDS:
                self.sym = Lexer.WORDS[ident]
            self.value = ident
            self.has_command = True

        elif self.ch.isalpha() or self.ch.isspace() or self.ch.isdigit():
            ident = ''
            while ((self.ch.isalpha() or self.ch.isspace()
                   or self.ch.isdigit() or self.ch == "'"
                   or self.ch == "*" or self.ch == "-" or self.ch == "+")
                   and self.sym is None):
                ident = ident + self.ch
                self.getc()
            self.value = ident
            self.sym = SymbolAndCommand.ID

        elif self.ch == "\"":  # строка в кавычках
            ident = ''
            self.getc()
            while (self.ch != "\"") and self.sym is None and self.ch is not None:
                ident = ident + self.ch
                self.getc()
            self.getc()
            self.value = ident
            self.sym = SymbolAndCommand.STRING

        elif self.ch in Lexer.SYMBOLS:  # символ окончания строки
            self.has_command = False
            ident = ''
            while self.ch in Lexer.SYMBOLS:
                ident += self.ch
                self.getc()
            self.value = ident
            self.sym = SymbolAndCommand.PUNCTUATION
        return self.value.rstrip(), self.sym


class Interpretator:
    def __init__(self, text, io = IO()):
        lexer = Lexer(text)
        self.tokens = []
        while lexer.index <= len(lexer.text):
            next_tok = lexer.next_tok()
            self.tokens.append(next_tok)
            print(next_tok)

        self.in_method = False
        self.in_what_method = []
        self.is_exectute_if = False
        self.method = {}
        self.classes = {}
        self.variables = {}
        self.circle = []  # имя переменной, больше/меньше, величина
        self.circle_ind = None
        self.io = io

    def execute(self):
        ind = 0
        while ind < len(self.tokens):
            if (self.in_method and
                    self.tokens[ind][1] != SymbolAndCommand.ENDMETHOD):
                ind += 1
                continue

            elif self.tokens[ind][1] == SymbolAndCommand.APPROPRIATION:
                ind_start = ind
                should_remove = [
                    " was ", " is ", " has ",
                    " had ", " like ", " likes ", " liked "
                    ]
                operations = [
                    " plus ", " added to ", ' minus ', 
                    " without ", ' times ', ' multiplied with ',
                    ' divided by ']
                for word in should_remove:
                    if self.tokens[ind+1][0].find(word) != -1:
                        variable, value = self.tokens[ind + 1][0].split(word)
                        if variable in self.variables:
                            if (self.variables[variable][0] == SymbolAndCommand.NUM
                                    and value.isdigit()):
                                self.variables[variable][1] = int(value)
                            elif value in self.variables:
                                self.variables[variable][1] = (
                                    self.variables[value][1])
                            elif value in self.method:
                                self.method[value]['result'] = variable
                                save_ind = ind + 2
                                self.method[value]['save_ind'] = save_ind
                                ind = self.method[value]['start_ind']
                                self.in_what_method.append(value)
                                # print("call method")
                            elif value.find(" using ") != -1:
                                value, args = value.split(" using ")
                                args = args.split(' and ')

                                self.method[value]['result'] = variable
                                save_ind = ind + 2
                                self.method[value]['save_ind'] = save_ind
                                ind = self.method[value]['start_ind']
                                self.in_what_method.append(value)
                                for i in range(len(self.method[value]['using_values'])):
                                    self.variables[self.method[value]['using_values'][i]] = self.variables[args[i]]

                                # print("call method")

                            else:
                                this_operation = None
                                for operation in operations:
                                    if value.find(operation) != -1:
                                        this_operation = Lexer.WORDS[operation[1:-1]]
                                        first, second = value.split(operation)
                                        if first in self.variables:
                                            first = self.variables[first][1]
                                        elif first.isdigit():
                                            first = int(first)
                                        if second in self.variables:
                                            second = self.variables[second][1]
                                        elif second.isdigit():
                                            second = int(second)
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

                                
                        else:
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
                        break
                if ind_start == ind:
                    ind += 2
                #print("did you know", self.variables)

            elif self.tokens[ind][1] == SymbolAndCommand.PUNCTUATION:
                ind += 1
                # print("punct")

            elif self.tokens[ind][1] == SymbolAndCommand.PRINT:
                text = ""
                ind += 1
                while self.tokens[ind][1] != SymbolAndCommand.PUNCTUATION:
                    if (self.tokens[ind][1] == SymbolAndCommand.STRING or
                        self.tokens[ind][1] == SymbolAndCommand.NUM or
                        self.tokens[ind][0] not in self.variables):
                        text += self.tokens[ind][0]
                    else:
                        text += str(self.variables[self.tokens[ind][0]][1])
                    ind += 1
                self.io.print_line(text)
            elif self.tokens[ind][1] == SymbolAndCommand.READ:
                value = self.io.get_line()
                if self.variables[self.tokens[ind+1][0]][0] == SymbolAndCommand.STRING:
                    self.variables[self.tokens[ind+1][0]][1] = value
                elif self.variables[self.tokens[ind+1][0]][0] == SymbolAndCommand.NUM:
                    self.variables[self.tokens[ind+1][0]][1] = int(value)
                # print("READ ", self.variables)
                ind += 2
            elif self.tokens[ind][1] == SymbolAndCommand.ASK:
                self.io.print_line(self.tokens[ind+2][0])
                value = self.io.get_line()
                if self.variables[self.tokens[ind+1][0]][0] == SymbolAndCommand.STRING:
                    self.variables[self.tokens[ind+1][0]][1] = value
                elif self.variables[self.tokens[ind+1][0]][0] == SymbolAndCommand.NUM:
                    self.variables[self.tokens[ind+1][0]][1] = int(value)
                # print("ASK ", variables)
                ind += 3

            elif self.tokens[ind][1] == SymbolAndCommand.PLUS:
                should_replace = [" to ", " and "]
                for word in should_replace:
                    if self.tokens[ind+1][0].find(word) != -1:
                        res_replace = self.tokens[ind+1][0].replace(word, ".")
                        first, second = res_replace.split(".")
                        try:
                            self.variables[second][1] += int(first)
                        except ValueError:
                            self.variables[second][1] += (
                                self.variables[first][1])
                    break
                ind += 2
                # print(self.variables, "plus")
            elif self.tokens[ind][1] == SymbolAndCommand.MINUS:
                should_replace = [" from ", " and "]
                for word in should_replace:
                    if self.tokens[ind+1][0].find(word) != -1:
                        res_replace = self.tokens[ind+1][0].replace(word, ".")
                        first, second = res_replace.split(".")
                        try:
                            self.variables[second][1] -= int(first)
                        except ValueError:
                            self.variables[second][1] -= (
                                self.variables[first][1])
                        break
                ind += 2
                # print(self.variables, "minus")
            elif self.tokens[ind][1] == SymbolAndCommand.MULTIPLY:
                should_replace = [" and "]
                for word in should_replace:
                    if self.tokens[ind+1][0].find(word) != -1:
                        res_replace = self.tokens[ind+1][0].replace(word, ".")
                        first, second = res_replace.split(".")
                        try:
                            self.variables[second][1] *= int(first)
                        except ValueError:
                            self.variables[second][1] *= (
                                self.variables[first][1])
                        break
                ind += 2
                # print(self.variables, "multiply")
            elif self.tokens[ind][1] == SymbolAndCommand.DEVIDE:
                should_replace = [" by ", " and "]
                for word in should_replace:
                    if self.tokens[ind+1][0].find(word) != -1:
                        res_replace = self.tokens[ind+1][0].replace(word, ".")
                        first, second = res_replace.split(".")
                        try:
                            self.variables[first][1] = math.floor(
                                self.variables[first][1] / int(second))
                        except ValueError:
                            self.variables[first][1] = math.floor(
                                self.variables[first][1] / self.variables[second][1])
                        break
                ind += 2
                # print(self.variables, "devide")

            elif self.tokens[ind][1] == SymbolAndCommand.WHILE:
                string = self.tokens[ind + 1][0]
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
                    ' not more ', ' not greater ',' not less ', 
                    ' less than ', ' more than ', ' greater than ',
                    " not "
                    ]  # дополнить равно
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
                self.circle_ind = ind + 2
                ind += 2
                # print("start while")
            elif self.tokens[ind][1] == SymbolAndCommand.ENDWHILE:
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
                    ind += 1
                    # print("finish while")
                else:
                    ind = self.circle_ind

            elif self.tokens[ind][1] == SymbolAndCommand.STARTMETHOD:
                self.method_with_name_return_args = (
                    self.tokens[ind+1][0].replace('about ', ""))
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
                    'start_ind': ind + 3,
                    'return_type': return_type,
                    'using_values': using_values,
                }
                self.in_method = True
                ind += 2
                # print("start method")
            elif self.tokens[ind][1] == SymbolAndCommand.MAINMETHOD:
                name = self.tokens[ind+1][0].replace('about ', "")
                self.method[name] = {
                    'is_main': True,
                    'start_ind': ind + 3,
                    'return_type': None,
                    'using_values': None,
                }
                ind += 2
                # print("start main")
            elif self.tokens[ind][1] == SymbolAndCommand.ENDMETHOD:
                name = self.tokens[ind+1][0]
                if len(self.method[name]) == 4:
                    self.in_method = False
                    self.method[name]['finish_ind'] = ind
                    ind += 2
                else:
                    tmp = ind
                    ind = self.method[name]['save_ind']
                    self.method[name].pop('save_ind')
                #  print("end method")
            elif self.tokens[ind][1] == SymbolAndCommand.CALLMETHOD:               
                name_method_with_args = self.tokens[ind + 1][0]
                if name_method_with_args.find(" using ") != -1:
                    name_method, args = name_method_with_args.split(" using ")
                    args = args.split(', ')
                    for i in range(len(self.method[name_method]['using_values'])):
                        if args[i] in self.variables:
                            self.variables[self.method[name_method]['using_values'][i]] = self.variables[args[i]]
                        elif args[i].isdigit():
                            self.variables[self.method[name_method]['using_values'][i]] = [SymbolAndCommand.NUM, int(args[i])]
                else:
                    name_method = name_method_with_args
                save_ind = ind + 2
                self.method[name_method]['save_ind'] = save_ind
                ind = self.method[name_method]['start_ind']
                self.in_what_method.append(name_method)
                # print("call method")
            elif self.tokens[ind][1] == SymbolAndCommand.RETURN:
                answer = self.tokens[ind + 1][0]
                try:
                    answer = int(answer)
                except ValueError:
                    if answer in self.variables:
                        answer = self.variables[answer][1]
                ind += 2
                name_method = self.in_what_method.pop()
                name_value = self. method[name_method]['result']
                self.method[name_method].pop('result')

                self.variables[name_value][1] = answer
                # print("return", answer)

            elif self.tokens[ind][1] == SymbolAndCommand.STARTCLASS:
                tmp = []
                ind += 1
                while self.tokens[ind][1] != SymbolAndCommand.PUNCTUATION:
                    tmp.append(self.tokens[ind][0])
                    ind += 1
                tmp.append(ind + 3)
                self.classes[self.tokens[ind + 1][0]] = tmp
                ind += 3
                # print("start class")
            elif self.tokens[ind][1] == SymbolAndCommand.ENDCLASS:
                ind += 2
                # print("end class")

            elif self.tokens[ind][1] == SymbolAndCommand.IF:
                condition = self.tokens[ind + 1][0]
                should_replace = [" was ", " is ", " has ", " had "]
                for word in should_replace:
                    if condition.find(word) != -1:
                        first, second = condition.split(word)
                        second = second.replace(" then", "")
                        try:
                            first = int(first)
                        except ValueError:
                            if first in self.variables:
                                first = self.variables[first][1]
                        try:
                            second = int(second)
                        except ValueError:
                            if second in self.variables:
                                second = self.variables[second][1]
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
                        try:
                            first = int(parts[0])
                        except ValueError:
                            first = self.variables[parts[0]][1]
                        try:
                            second = int(parts[1])
                        except ValueError:
                            second = self.variables[parts[1]][1]
                        break
                if operation is None:
                    operation = SymbolAndCommand.EQUALS
                if (operation == SymbolAndCommand.MORE and
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
                        first != second):
                    ind += 2
                    self.is_exectute_if = True
                else:
                    ind += 2
                    while (self.tokens[ind][1] != SymbolAndCommand.ELSE
                           and self.tokens[ind][1] != SymbolAndCommand.ENDIF):
                        ind += 1
            elif self.tokens[ind][1] == SymbolAndCommand.ENDIF:
                ind += 1
                self.is_exectute_if = False
                # print("end if")
            elif self.tokens[ind][1] == SymbolAndCommand.ELSE:
                if self.is_exectute_if:
                    while self.tokens[ind][1] != SymbolAndCommand.ENDIF:
                        ind += 1
                ind += 1
                self.is_exectute_if = False
                # print("else if")

            else:
                print(self.tokens[ind][0])
def main():
    if len(sys.argv) == 2:
        name_file = sys.argv[1]
        if os.path.exists(name_file):
            with open(name_file, 'r') as f:
                text = f.read().rstrip()
    else:
        text = input()
        while not text.rstrip().endswith('stop'):
            text += input()
        text = text.rstrip()[:-4]
                
    i = Interpretator(text, IO())
    i.execute()

    print(i.variables)
    print(i.method)
    print(i.classes)


if __name__ == "__main__":
    main()
