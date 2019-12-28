from lexer import Lexer
from symbolAndCommand import TOKEN_TYPES
import sys
from const import Const


class Translator:
    def __init__(self, text, name_class):
        if text == "":
            raise Exception("Пустой текст")
        self.tokens = list(Lexer(text))
        self.ind = 0
        self.variables = {}
        self.method = {}
        self.java_text = []
        self.name_class = name_class
        
        self.dict_function = {
            TOKEN_TYPES.APPROPRIATION: self.approptiate_value,
            TOKEN_TYPES.PUNCTUATION: self.punctuation,
            TOKEN_TYPES.READ: self.read_line,
            TOKEN_TYPES.ASK: self.ask_line,

            TOKEN_TYPES.WHILE: self.start_while,
            TOKEN_TYPES.ENDWHILE: self.check_ending_while,

            TOKEN_TYPES.STARTMETHOD: self.start_method,
            TOKEN_TYPES.MAINMETHOD: self.keep_info_main_method,
            TOKEN_TYPES.ENDMETHOD: self.end_method,
            TOKEN_TYPES.CALLMETHOD: self.call_method,
            TOKEN_TYPES.RETURN: self.return_value_from_method,

            TOKEN_TYPES.STARTCLASS: self.start_class,
            TOKEN_TYPES.ENDCLASS: self.end_class,

            TOKEN_TYPES.IF: self.start_if,
            TOKEN_TYPES.ENDIF: self.end_if,
            TOKEN_TYPES.ELSE: self.else_if
        }
    
    
    def approptiate_value(self):
        for word in Const.SHOULD_IGNORE:
            if word in self.tokens[self.ind+1].command:
                variable, value = self.tokens[self.ind + 1].command.split(word)
                if variable.replace(' ', '_') in self.variables:
                    variable = variable.replace(' ', '_')
                    if (self.variables[variable] is not None and self.variables[variable][0] == TOKEN_TYPES.NUM
                            and value.isdigit()):
                        self.java_text.append(f"{variable} = {value};")
                    elif (self.variables[variable] is not None and self.variables[variable][0] == TOKEN_TYPES.STRING):
                        self.java_text.append(f'{variable} = "{value}";')
                    elif value.replace(' ', '_') in self.variables:
                        value = value.replace(' ', '_')
                        self.java_text.append(f"{variable} = {value};")
                    elif value.replace(' ', '_') in self.method or " using " in value:
                        has_args = False
                        if " using " in value:
                            has_args = True
                        self.approptiate_value_method(value, variable, has_args)
                    else:
                        variable = variable.replace(' ', '_')
                        self.approptiate_value_operation(value, variable)
                else:
                    self.init_variable(variable, value)
                break
        self.ind += 2

    def init_variable(self, variable, value):
        for types in Const.SHOULD_FIND_TYPE:
            if types in value:
                this_type = Lexer.WORDS[types]
                value = value[
                    value.find(types) + len(types) + 1:]
                if (this_type == TOKEN_TYPES.NUM and
                        value.rstrip() != ""):
                    value = int(value)
                elif this_type == TOKEN_TYPES.STRING:
                    value = f'"{value}"'
                variable = variable.replace(' ', '_')
                self.variables[variable] = [
                    this_type, value]
                if value != "":
                    self.java_text.append(f'var {variable} = {value};')
                else:
                    self.java_text.append(f'{types} {variable};')
                break

    def approptiate_value_operation(self, value, variable):
        this_operation = None
        for operation in Const.OPERATIONS_STR:
            if operation in value:
                this_operation = Lexer.WORDS[operation[1:-1]]
                first, second = value.split(operation)
                break
        if this_operation is None:
            self.java_text.append(value)
        else:            
            first = first.replace(' ', '_')
            second = second.replace(' ', '_')
            self.java_text.append(f'{variable} = {first} {Const.OPERATION[this_operation]} {second};')

    def approptiate_value_method(self, value, variable, has_args):
        arguments = ""
        if has_args:
            value, args = value.split(" using ")       
            arguments = args.replace(' and ', ', ')
        value = value.replace(' ', '_')
        self.java_text.append(f"{variable} = {value}({arguments});")

    def start_method(self):
        method_with_name_return_args = (
            self.tokens[self.ind + 1].command.replace('about ', ""))
        return_type = None
        arguments = ""
        using_values = None
        if ' with ' in method_with_name_return_args:
            name, method_with_return_args = (
                method_with_name_return_args.split(' with '))
            if ' using ' in method_with_return_args:
                return_type, args = (
                    method_with_return_args.split(' using '))
                using_values = args.split(" and ")
            else:
                return_type = method_with_return_args   
        elif ' using ' in method_with_name_return_args:
            name, args = (
                method_with_name_return_args.split(' using '))
            using_values = args.split(" and ")
        else:
            name = method_with_name_return_args
        name = name.replace(' ', '_')
        if using_values is None:
            using_values_with_types = None
        else:
            using_values_with_types = []
            for value in using_values:
                for types in Const.SHOULD_FIND_TYPE:
                    if types in value:
                        ind = len(types) + 1
                        val = value[ind:].replace(' ', '_')
                        using_values_with_types.append([val, types])
                        arguments += types + " " + val + ", "
                        self.variables[val] = None
                        break
            arguments = arguments[:-2]
        self.method[name] = None
        if return_type is None:
            return_type = 'void'
        self.java_text.append(f"public static {return_type} {name}({arguments})" + " {")
        self.ind += 3

    def start_if(self):
        condition = self.tokens[self.ind + 1].command
        for word in Const.SHOULD_REPLACE:
            if word in condition:
                first, second = condition.split(word)
                second = second.replace(" then", "")
                condition = condition.replace(word, " ")
                break
        operation = TOKEN_TYPES.EQUALS
        for e in Const.COMPARATORS:
            if e in condition:
                condition = condition.replace(" then", "")
                first, second = condition.split(e)
                operation = Lexer.WORDS[e[1:-1]]
                break
        second_sep = first_sep = ""
        first = first.replace(' ', '_')
        second = second.replace(' ', '_')
        equals = f' {Const.OPERATION[operation]} {second}'
        if not second.isdigit() and second not in self.variables:
            second_sep = '"'
            equals = f".equals({second_sep}{second}{second_sep})"
        if not first.isdigit() and first not in self.variables:
            first_sep = '"'
            equals = f".equals({second_sep}{second}{second_sep})"
        if self.java_text[-1] == 'else':
            self.java_text[-1] += f' if ({first_sep}{first}{first_sep}{equals})' + " {"  
        else:
            self.java_text.append(f'if ({first_sep}{first}{first_sep}{equals})' + " {")
        self.ind += 3

    def call_method(self):
        name_method_with_args = self.tokens[self.ind + 1].command
        arguments = ""
        if ' using ' in name_method_with_args:
            name_method, args = name_method_with_args.split(" using ")
            arguments = args.replace(' and ', ', ')
        else:
            name_method = name_method_with_args
        name_method = name_method.replace(' ', '_')
        self.java_text.append(f"{name_method}({arguments});")
        self.ind += 2

    def start_while(self):
        string = self.tokens[self.ind + 1].command
        for word in Const.SHOULD_REPLACE:
            if word in string:
                ind_find = string.find(word)
                name = string[: ind_find].replace(' ', '_')
                value = string[ind_find + len(word):]
                string = string.replace(word, " ")
                break     
        operation = Const.OPERATION[TOKEN_TYPES.EQUALS]
        for eq in Const.COMPARATORS:
            ind_find = string.find(eq)
            if ind_find != -1:
                name = string[: ind_find].replace(' ', '_')
                value = string[ind_find + len(eq):]
                operation = Const.OPERATION[Lexer.WORDS[eq[1:-1]]]
                break
        self.java_text.append(f'while ({name} {operation} {value})'" {")
        self.ind += 2

    def make_arithmetic(self, should_replace, operation):
        values = self.tokens[self.ind + 1].command
        for word in should_replace:
            if word in values:
                first, second = values.split(word)
                if operation == TOKEN_TYPES.DIVIDE:
                    first, second = second, first
        first = first.replace(' ', '_')
        second = second.replace(' ', '_')
        self.java_text.append(f'{second} {Const.OPERATION[operation]}= {first};')
        self.ind += 2

    def start_class(self):
        self.ind += 3
        self.java_text.append("import java.util.Scanner;")
        self.java_text.append(f"public class {self.name_class} " + "{")
        self.ind += 2

    def end_class(self):
        self.java_text.append("}")
        self.ind += 3

    def keep_info_main_method(self):
        self.java_text.append("public static void main(String[] args) {")
        self.ind += 3
    
    def end_method(self):
        self.java_text.append("}")
        self.ind += 3
    
    def punctuation(self):
        self.ind += 1

    def else_if(self):
        self.java_text.append("}")
        self.java_text.append("else")
        self.ind += 2
        if not self.tokens[self.ind].command.startswith('if'):
            self.java_text[-1] += " {"

    def end_if(self):
        self.java_text.append("}")
        self.ind += 1

    def return_value_from_method(self):
        self.java_text.append(f"return {self.tokens[self.ind + 1].command.replace(' ', '_')};")
        self.ind += 2

    def check_ending_while(self):
        self.java_text.append("}")
        self.ind += 1

    def read_line(self):
        if not self.has_scanner:
            self.java_text.append(f'Scanner in = new Scanner(System.in);')
            self.has_scanner = True
        variable = self.tokens[self.ind + 1].command.replace(' ', '_')
        if self.variables[variable][0] == TOKEN_TYPES.STRING:
            self.java_text.append(f'{variable} = in.next();')
        elif self.variables[variable][0] == TOKEN_TYPES.NUM:
            self.java_text.append(f'{variable} = in.nextInt();')
        self.ind += 2 
    
    def print_line(self, command, type_command):
        text = ""
        self.ind += 1
        command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command 
        while type_command != TOKEN_TYPES.PUNCTUATION:
            if type_command == TOKEN_TYPES.STRING:
                text += f'"{command}" + '
            else:
                command = command.replace(' ', '_')
                text += f'{command} + '
            self.ind += 1
            command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command 
        self.java_text.append(f'System.out.println({text[:-3]});')

    def ask_line(self):
        if self.tokens[self.ind + 2].type_command == TOKEN_TYPES.STRING:
            self.java_text.append(f'System.out.println("{self.tokens[self.ind + 2].command}");')
        else:
            self.java_text.append(f'System.out.println({self.tokens[self.ind + 2].command});')
        self.read_line()
        self.ind += 1

    def translate(self):
        self.has_scanner = False
        while self.ind < len(self.tokens):
            command, type_command = self.tokens[self.ind].command, self.tokens[self.ind].type_command
            if type_command == TOKEN_TYPES.PRINT: 
                self.print_line(command, type_command)
            elif (type_command == TOKEN_TYPES.PLUS
                    or type_command == TOKEN_TYPES.MINUS
                    or type_command == TOKEN_TYPES.MULTIPLY
                    or type_command == TOKEN_TYPES.DIVIDE):
                self.make_arithmetic(
                    Const.DICT_REPLACE[type_command], type_command)
            else:
                try:
                    self.dict_function.get(type_command)()
                except KeyError:
                    print("Wrong token: " + self.tokens[self.ind].command)                
                    sys.exit(2)
    
    def correct_text(self):
        self.right_text = []
        for string in self.java_text:
            string = string.replace('the number', 'int').replace('the word', 'String').replace("'", "_")
            self.right_text.append(string)
        return "\n".join(self.right_text)
