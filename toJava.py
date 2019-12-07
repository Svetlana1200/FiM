from lexer import Lexer
from symbolAndCommand import TOKEN_TYPES
import sys
from interpretator import Interpretator


class ToJava:
    OPERATION = {
        TOKEN_TYPES.PLUS: "+",
        TOKEN_TYPES.MINUS: "-",
        TOKEN_TYPES.MULTIPLY: "*",
        TOKEN_TYPES.DIVIDE: "/",
        TOKEN_TYPES.MORE: '>',
        TOKEN_TYPES.LESS: '<',
        TOKEN_TYPES.EQLESS: '<=',
        TOKEN_TYPES.EQMORE: ">=",
        TOKEN_TYPES.EQUALS: "==",
        TOKEN_TYPES.NOTEQ: "!="
    }

    def __init__(self, text):
        if text == "":
            print("ПУстой текст")
            sys.exit(3)
        self.tokens = list(Lexer(text))
        self.ind = 0
        self.variables = {}
        self.method = {}
        #for token in self.tokens:
        #    print(token.command, token.type_command)


    def approptiate_value(self):
        ind_start = self.ind
        for word in Interpretator.should_ignore:
            if word in self.tokens[self.ind+1].command:
                variable, value = self.tokens[self.ind + 1].command.split(word)
                if variable in self.variables:
                    if (self.variables[variable] is not None and self.variables[variable][0] == TOKEN_TYPES.NUM
                            and value.isdigit()):
                        print(f"{variable} = {value}")
                        #self.approptiate_nuber(value, variable)
                    elif value in self.variables:
                        
                        print(f"{variable} = {value}")
                        #self.approptiate_value_variable(value, variable)
                    elif value in self.method or " using " in value:
                        has_args = False
                        if " using " in value:
                            has_args = True
                        value = self.approptiate_value_method(
                            value, variable, has_args)
                    else:
                        self.approptiate_value_operation(value, variable)
                else:
                    self.init_variable(variable, value)
                break
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
                print(f'var {variable} = {value}')
                break

    def approptiate_value_operation(self, value, variable):
        this_operation = None
        for operation in Interpretator.operations:
            if operation in value:
                this_operation = Lexer.WORDS[operation[1:-1]]
                first, second = value.split(operation)
                break
        if this_operation is None: ##################
            print(value)
        else:
            print(f'{variable} = {first} {ToJava.OPERATION[this_operation]} {second}')

    def approptiate_value_variable(self, value, variable):
        self.variables[variable][1] = self.variables[value][1]

    def approptiate_nuber(self, value, variable):
        self.variables[variable][1] = int(value)

    def approptiate_value_method(self, value, variable, has_args):
        arguments = ""
        if has_args:
            value, args = value.split(" using ")
            args = args.split(' and ')
            arguments = ", ".join(args)
        print(f"{variable} = {value}({arguments[:-2]})")
        return value

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
                for value in using_values:
                    self.variables[value] = None
                arguments = ", ".join(using_values)
                print(f"public {return_type} {name}({arguments})" + " {")
            else:
                return_type = self.method_with_return_args
                print(f"public {return_type} {name}()" + " {")
        elif ' using ' in self.method_with_name_return_args:
            name, args = (
                self.method_with_name_return_args.split(' using '))
            using_values = args.split(" and ")
            for value in using_values:
                    self.variables[value] = None
            arguments = ", ".join(using_values)
            print(f"public void {name}({arguments})" + " {")
        self.method[name] = {
            'is_main': False,
            'start_ind': self.ind + 3,
            'return_type': return_type,
            'using_values': using_values,
        }
        self.in_method = True
        self.ind += 2

    def start_if(self):
        condition = self.tokens[self.ind + 1].command
        for word in Interpretator.should_replace:
            if word in condition:
                first, second = condition.split(word)
                second = second.replace(" then", "")
                condition = condition.replace(word, " ")
                break
        operation = None

        for e in Interpretator.comparators:
            if e in condition:
                operation = Lexer.WORDS[e[1:-1]]
                condition = condition.replace(" then", "")
                parts = condition.split(e)
                break
        if operation is None:
            operation = TOKEN_TYPES.EQUALS
        ToJava.print_if_condition(operation, first, second)
        self.ind += 2

    @staticmethod
    def print_if_condition(operation, first, second):
        print (f'if ({first} {ToJava.OPERATION[operation]} {second})' + " {")

    def call_method(self):
        name_method_with_args = self.tokens[self.ind + 1].command
        if ' using ' in name_method_with_args:
            name_method, args = name_method_with_args.split(" using ")
            args = args.split(', ')
            arguments = ""
            for i in range(len(self.method[name_method]['using_values'])):
                if args[i] in self.variables:
                    self.variables[
                        self.method[name_method]['using_values'][i]
                        ] = self.variables[args[i]]
                elif args[i].isdigit():
                    self.variables[
                        self.method[name_method]['using_values'][i]
                        ] = [TOKEN_TYPES.NUM, int(args[i])]
                arguments += args[i] + ", "
            
            print(f"{name_method}({arguments[:-2]})")
        else:
            name_method = name_method_with_args
            print(f"{name_method}()")
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
                value = string[ind_find + len(eq):]
                print(f'while ({name} {ToJava.OPERATION[Lexer.WORDS[eq[1:-1]]]} {value})' + " {")
                break
        if not find_operation:
            print(f'while {name} {TToJava.OPERATION[OKEN_TYPES.EQUAL]} {value}'" {")
        self.ind += 2

    def make_arithmetic(self, should_replace, operation):
        values = self.tokens[self.ind + 1].command
        for word in should_replace:
            if word in values:
                res_replace = values.replace(word, ".")
                first, second = res_replace.split(".")
                if operation == TOKEN_TYPES.DIVIDE:
                    first, second = second, first
        print(f'{second} {ToJava.OPERATION[operation]}= {first}')
        self.ind += 2

    def print_line(self, command, type_command):
        text = ""
        self.ind += 1
        command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command 
        while type_command != TOKEN_TYPES.PUNCTUATION:
            if type_command == TOKEN_TYPES.STRING:
                text += f'"{command}" + '
            else:
                text += f'{command} + '
            self.ind += 1
            command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command 
        print(f'System.out.println({text[:-3]})')


    def translate(self):
        has_scanner = False
        while self.ind < len(self.tokens):
            command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command
            if type_command == TOKEN_TYPES.STARTCLASS:
                self.ind += 3
                name_class = self.tokens[self.ind].command
                print(f"public class {name_class} " + "{")
                self.ind += 2
            elif type_command == TOKEN_TYPES.ENDCLASS:
                print("}")
                self.ind += 3
            elif type_command == TOKEN_TYPES.MAINMETHOD:
                print("public void main() {")
                self.ind += 3
            elif type_command == TOKEN_TYPES.ENDMETHOD:
                print("}")
                self.ind += 3
            elif type_command == TOKEN_TYPES.PUNCTUATION:
                #print(";")
                self.ind += 1
            elif type_command == TOKEN_TYPES.APPROPRIATION:
                self.approptiate_value()
            elif type_command == TOKEN_TYPES.STARTMETHOD:
                self.start_method()
            elif type_command == TOKEN_TYPES.IF:
                self.start_if()
            elif type_command == TOKEN_TYPES.ELSE:
                print("}")
                print("else")
                self.ind += 1
            elif type_command == TOKEN_TYPES.ENDIF:
                print("}")
                self.ind += 1
            elif type_command == TOKEN_TYPES.RETURN:
                print(f"return {self.tokens[self.ind + 1].command}")
                self.ind += 2
            elif type_command == TOKEN_TYPES.CALLMETHOD:
                self.call_method()

            elif type_command == TOKEN_TYPES.WHILE:
                self.start_while()
            elif type_command == TOKEN_TYPES.ENDWHILE:
                print("}")
                self.ind += 1
            
            elif (type_command == TOKEN_TYPES.PLUS
                    or type_command == TOKEN_TYPES.MINUS
                    or type_command == TOKEN_TYPES.MULTIPLY
                    or type_command == TOKEN_TYPES.DIVIDE):
                should_replace = Interpretator.dict_replace[type_command]
                self.make_arithmetic(should_replace, type_command)
            
            elif type_command == TOKEN_TYPES.PRINT:
                self.print_line(command, type_command)

            elif type_command == TOKEN_TYPES.READ:
                if not has_scanner:
                    print(f'Scanner in = new Scanner(System.in)')
                    has_scanner = True
                variable = self.tokens[self.ind + 1].command
                if self.variables[variable][0] == TOKEN_TYPES.STRING:
                    print(f'String {variable} = in.nextInt()')
                elif self.variables[variable][0] == TOKEN_TYPES.NUM:
                    print(f'Int {variable} = in.nextInt()')
                self.ind += 2 
            elif type_command == TOKEN_TYPES.ASK:
                if self.tokens[self.ind + 2].type_command == TOKEN_TYPES.STRING:
                    print(f'System.out.println("{self.tokens[self.ind + 2].command}")')
                else:
                    print(f'System.out.println({self.tokens[self.ind + 2].command})')
                if not has_scanner:
                    print(f'Scanner in = new Scanner(System.in)')
                    has_scanner = True
                variable = self.tokens[self.ind + 1].command
                if self.variables[variable][0] == TOKEN_TYPES.STRING:
                    print(f'String {variable} = in.nextInt()')
                elif self.variables[variable][0] == TOKEN_TYPES.NUM:
                    print(f'Int {variable} = in.nextInt()')
                self.ind += 3
            else:
                print("Wrong token: " + command)                
                sys.exit(2)\
            


