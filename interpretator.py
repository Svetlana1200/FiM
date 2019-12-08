from lexer import Lexer
from symbolAndCommand import TOKEN_TYPES
import math
import sys


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


class Interpretator:
    should_ignore = [
            " was ", " is ", " has ",
            " had ", " like ", " likes ", " liked "
            ]
    should_replace = [
            " was ", " is ", " has ",
            " had ", " like ", " likes ", " liked "]
    comparators = [
            ' no less than ', ' no more than ', ' no greater than ',
            ' not more ', ' not greater ', ' not less ',
            ' more than ', ' greater than ', ' less than ', ' not ',
            ]
    operations = [
            " plus ", " added to ", ' minus ',
            " without ", ' times ', ' multiplied with ',
            ' divided by ']
    dict_replace = {
        TOKEN_TYPES.PLUS: [" to ", " and "],
        TOKEN_TYPES.MINUS: [" from ", " and "],
        TOKEN_TYPES.MULTIPLY: [" and "],
        TOKEN_TYPES.DIVIDE: [" by ", " and "],
    }

    should_find_type = ["the number", "the word"]

    def __init__(self, text, io=IO()):
        if text == "":
            print("ПУстой текст")
            sys.exit(3)
        self.tokens = list(Lexer(text))
        #for token in self.tokens:
            #print(token.command, token.type_command)

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
        for word in Interpretator.should_ignore:
            if word in self.tokens[self.ind+1].command:
                variable, value = self.tokens[self.ind + 1].command.split(word)
                if variable in self.variables:
                    if (self.variables[variable][0] == TOKEN_TYPES.NUM
                            and value.isdigit()):
                        self.approptiate_nuber(value, variable)
                    elif value in self.variables:
                        self.approptiate_value_variable(value, variable)
                    elif value in self.method or " using " in value:
                        has_args = False
                        if " using " in value:
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
        for types in Interpretator.should_find_type:
            if types in value:
                this_type = Lexer.WORDS[types]
                value = value[
                    value.find(types) + len(types) + 1:]
                if (this_type == TOKEN_TYPES.NUM and
                        value.rstrip() != ""):
                    value = int(value)
                self.variables[variable] = [
                    this_type, value]
                break

    def approptiate_value_operation(self, value, variable):
        this_operation = None
        for operation in Interpretator.operations:
            if operation in value:
                this_operation = Lexer.WORDS[operation[1:-1]]
                first, second = value.split(operation)
                first, _was_conver = self.try_conver_to_int(first)
                second, _was_conver = self.try_conver_to_int(second)
                break
        if this_operation is None:
            self.variables[variable][1] = value
        elif this_operation == TOKEN_TYPES.MINUS:
            self.variables[variable][1] = first - second
        elif this_operation == TOKEN_TYPES.MULTIPLY:
            self.variables[variable][1] = first * second
        elif this_operation == TOKEN_TYPES.PLUS:
            self.variables[variable][1] = first + second
        elif this_operation == TOKEN_TYPES.DIVIDE:
            self.variables[variable][1] = first // second

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
                    self.method[value]['using_values'][i][0] #################
                    ] = self.variables[args[i]]
        self.method[value]['result'] = variable
        self.method[value]['save_ind'] = self.ind + 2
        self.in_what_method.append(value)
        return value

    def print_line(self, command, type_command):
        text = ""
        self.ind += 1
        command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command 
        while type_command != TOKEN_TYPES.PUNCTUATION:
            if (type_command == TOKEN_TYPES.STRING or
                    type_command == TOKEN_TYPES.NUM or
                    command not in self.variables):
                text += command
            else:
                text += str(self.variables[command][1])
            self.ind += 1
            command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command 
        self.io.print_line(text)

    def read_line(self, variable=None):
        if variable is None:
            variable = self.tokens[self.ind + 1].command
        value = self.io.get_line()
        if self.variables[variable][0] == TOKEN_TYPES.STRING:
            self.variables[variable][1] = value
        elif self.variables[variable][0] == TOKEN_TYPES.NUM:
            self.variables[variable][1] = int(value)
        self.ind += 2

    def ask_line(self):
        self.io.print_line(self.tokens[self.ind + 2].command)
        self.read_line(self.tokens[self.ind + 1].command)
        self.ind += 1

    def make_arithmetic(self, should_replace, operation):
        values = self.tokens[self.ind + 1].command
        for word in should_replace:
            if word in values:
                res_replace = values.replace(word, ".")
                first, second = res_replace.split(".")
                if operation == TOKEN_TYPES.DIVIDE:
                    first, second = second, first
                first_value, _was_conver = self.try_conver_to_int(first, first)
        if operation == TOKEN_TYPES.PLUS:
            self.variables[second][1] += first_value
        elif operation == TOKEN_TYPES.MINUS:
            self.variables[second][1] -= first_value
        elif operation == TOKEN_TYPES.MULTIPLY:
            self.variables[second][1] *= first_value
        elif operation == TOKEN_TYPES.DIVIDE:
            self.variables[second][1] = self.variables[second][1] // first_value
        self.ind += 2

    def start_while(self):
        string = self.tokens[self.ind + 1].command
        for word in Interpretator.should_replace:
            if word in string:
                ind_find = string.find(word)
                name = string[: ind_find]
                value = string[ind_find + len(word):]
                string = string.replace(word, " ")
                break
        find_operation = False
        for eq in Interpretator.comparators:
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
            self.circle.append(TOKEN_TYPES.EQUALS)
            if value.isdigit():
                self.circle.append(int(value))
            else:
                self.circle.append(self.variables[value][1])
        self.circle_ind = self.ind + 2
        self.ind += 2

    def check_ending_while(self):
        if (self.circle[1] == TOKEN_TYPES.MORE and
                self.variables[self.circle[0]][1] <= self.circle[2] or
                self.circle[1] == TOKEN_TYPES.LESS and
                self.variables[self.circle[0]][1] >= self.circle[2] or
                self.circle[1] == TOKEN_TYPES.EQLESS and
                self.variables[self.circle[0]][1] > self.circle[2] or
                self.circle[1] == TOKEN_TYPES.EQMORE and
                self.variables[self.circle[0]][1] < self.circle[2] or
                self.circle[1] == TOKEN_TYPES.NOTEQ and
                self.variables[self.circle[0]][1] == self.circle[2] or
                self.circle[1] == TOKEN_TYPES.EQUALS and
                self.variables[self.circle[0]][1] != self.circle[2]):
            self.ind += 1
            # print("finish while")
        else:
            self.ind = self.circle_ind

    def start_if(self):
        condition = self.tokens[self.ind + 1].command
        for word in Interpretator.should_replace:
            if word in condition:
                first, second = condition.split(word)
                second = second.replace(" then", "")
                first, _was_convert = self.try_conver_to_int(first)
                second, _was_convert = self.try_conver_to_int(second)
                condition = condition.replace(word, " ")
                break
        operation = None

        for e in Interpretator.comparators:
            if e in condition:
                operation = Lexer.WORDS[e[1:-1]]
                condition = condition.replace(" then", "")
                parts = condition.split(e)
                first, _was_convert = self.try_conver_to_int(first, parts[0])
                second, _was_oinvert = self.try_conver_to_int(second, parts[1])
                break
        if operation is None:
            operation = TOKEN_TYPES.EQUALS
        if Interpretator.check_if_condition(operation, first, second):
            self.ind += 2
            self.is_exectute_if = True
        else:
            self.ind += 2
            type_command = self.tokens[self.ind].type_command

            while (type_command != TOKEN_TYPES.ELSE
                    and type_command != TOKEN_TYPES.ENDIF):
                self.ind += 1
                type_command = self.tokens[self.ind].type_command

    def start_method(self):
        self.method_with_name_return_args = (
            self.tokens[self.ind + 1].command.replace('about ', ""))
        name = None
        return_type = None
        using_values = None
        if ' with ' in self.method_with_name_return_args:
            name, self.method_with_return_args = (
                self.method_with_name_return_args.split(' with '))
            if ' using ' in self.method_with_return_args:
                return_type, args = (
                    self.method_with_return_args.split(' using '))
                using_values = args.split(" and ")
            else:
                return_type = self.method_with_return_args
        elif ' using ' in self.method_with_name_return_args:
            name, args = (
                self.method_with_name_return_args.split(' using '))
            using_values = args.split(" and ")
        if using_values is None:
            using_values_with_types = None
        else:
            using_values_with_types = [] ################
            for value in using_values:
                for types in Interpretator.should_find_type:
                    if types in value:
                        using_values_with_types.append([value[len(types) + 1:], types])

        self.method[name] = {
            'is_main': False,
            'start_ind': self.ind + 3,
            'return_type': return_type,
            'using_values': using_values_with_types,
        }
        self.in_method = True
        self.ind += 2

    def keep_info_main_method(self):
        name = self.tokens[self.ind+1].command.replace('about ', "")
        self.method[name] = {
            'is_main': True,
            'start_ind': self.ind + 3,
            'return_type': None,
            'using_values': None,
        }
        self.ind += 2

    def end_method(self):
        name = self.tokens[self.ind + 1].command
        if len(self.method[name]) == 4:
            self.in_method = False
            self.method[name]['finish_ind'] = self.ind
            self.ind += 2
        else:
            self.ind = self.method[name]['save_ind']
            self.method[name].pop('save_ind')

    def call_method(self):
        name_method_with_args = self.tokens[self.ind + 1].command
        if ' using ' in name_method_with_args:
            name_method, args = name_method_with_args.split(" using ")
            args = args.split(', ')
            for i in range(len(self.method[name_method]['using_values'])):
                if args[i] in self.variables:
                    self.variables[
                        self.method[name_method]['using_values'][i][0]
                        ] = self.variables[args[i]]
                elif args[i].isdigit():
                    self.variables[
                        self.method[name_method]['using_values'][i][0]
                        ] = [TOKEN_TYPES.NUM, int(args[i])]##############3
        else:
            name_method = name_method_with_args
        self.method[name_method]['save_ind'] = self.ind + 2
        self.ind = self.method[name_method]['start_ind']
        self.in_what_method.append(name_method)

    def return_value_from_method(self):
        answer = self.tokens[self.ind + 1].command
        answer, _was_conver = self.try_conver_to_int(answer)
        self.ind += 2
        name_method = self.in_what_method.pop()
        name_value = self.method[name_method]['result']
        self.method[name_method].pop('result')

        self.variables[name_value][1] = answer

    def start_class(self):
        tmp = []
        self.ind += 1
        command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command, 
        while type_command != TOKEN_TYPES.PUNCTUATION:
            tmp.append(command)
            self.ind += 1
            command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command, 
        tmp.append(self.ind + 3)
        self.classes[self.tokens[self.ind + 1].command] = tmp
        self.ind += 3

    def end_class(self):
        for name_class in self.classes.keys():
            value = self.classes[name_class][-2]
            if not self.try_conver_to_int(value)[1]:
                self.classes[name_class].append(self.ind)
        self.ind += 2

    @staticmethod
    def check_if_condition(operation, first, second):
        return (operation == TOKEN_TYPES.MORE and
                first > second or
                operation == TOKEN_TYPES.LESS and
                first < second or
                operation == TOKEN_TYPES.EQLESS and
                first <= second or
                operation == TOKEN_TYPES.EQMORE and
                first >= second or
                operation == TOKEN_TYPES.EQUALS and
                first == second or
                operation == TOKEN_TYPES.NOTEQ and
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
            command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command
            if (self.in_method and
                    type_command != TOKEN_TYPES.ENDMETHOD):
                self.ind += 1
                continue

            elif type_command == TOKEN_TYPES.APPROPRIATION:
                self.approptiate_value()
            elif type_command == TOKEN_TYPES.PUNCTUATION:
                self.ind += 1

            elif type_command == TOKEN_TYPES.PRINT:
                self.print_line(command, type_command)
            elif type_command == TOKEN_TYPES.READ:
                self.read_line()
            elif type_command == TOKEN_TYPES.ASK:
                self.ask_line()

            elif (type_command == TOKEN_TYPES.PLUS
                    or type_command == TOKEN_TYPES.MINUS
                    or type_command == TOKEN_TYPES.MULTIPLY
                    or type_command == TOKEN_TYPES.DIVIDE):
                should_replace = Interpretator.dict_replace[type_command]
                self.make_arithmetic(should_replace, type_command)

            elif type_command == TOKEN_TYPES.WHILE:
                self.start_while()
            elif type_command == TOKEN_TYPES.ENDWHILE:
                self.check_ending_while()

            elif type_command == TOKEN_TYPES.STARTMETHOD:
                self.start_method()
            elif type_command == TOKEN_TYPES.MAINMETHOD:
                self.keep_info_main_method()
            elif type_command == TOKEN_TYPES.ENDMETHOD:
                self.end_method()
            elif type_command == TOKEN_TYPES.CALLMETHOD:
                self.call_method()
            elif type_command == TOKEN_TYPES.RETURN:
                self.return_value_from_method()

            elif type_command == TOKEN_TYPES.STARTCLASS:
                self.start_class()
            elif type_command == TOKEN_TYPES.ENDCLASS:
                self.end_class()

            elif type_command == TOKEN_TYPES.IF:
                self.start_if()
            elif type_command == TOKEN_TYPES.ENDIF:
                self.ind += 1
                self.is_exectute_if = False
            elif type_command == TOKEN_TYPES.ELSE:
                if self.is_exectute_if:
                    while self.tokens[self.ind].type_command != TOKEN_TYPES.ENDIF:
                        self.ind += 1
                self.ind += 1
                self.is_exectute_if = False
            else:
                print("Wrong token: " + self.tokens[self.ind].command)                
                sys.exit(2)
