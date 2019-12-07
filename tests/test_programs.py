import os
import sys
import unittest


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from interpretator import Interpretator, BaseIO
from symbolAndCommand import TOKEN_TYPES


class IOTest(BaseIO):
    def __init__(self):
        self.value_print = ""
        self.value_get = ["cakes", "123"]

    def print_line(self, line):
        self.value_print += line + "\n"

    def get_line(self):
        return self.value_get.pop()


class GameTest(unittest.TestCase):
    def test_appropriation_number(self):
        text = '''Did you know that Spike was the number 12!'''
        i = Interpretator(text)
        i.execute() 
        self.assertDictEqual(i.variables, {'Spike': [TOKEN_TYPES.NUM, 12]})

    def test_appropriation_variable(self):
        text = '''Did you know that Spike was the number 12?
                Did you know that Rarity is the number?
                Now Rarity is Spike.'''
        i = Interpretator(text)
        i.execute() 
        self.assertDictEqual(i.variables, {'Spike': [TOKEN_TYPES.NUM, 12], 'Rarity': [TOKEN_TYPES.NUM, 12]})
    
    def test_words(self):
        text = '''Did you know that Spike likes the word cake?'''
        i = Interpretator(text)
        i.execute()    
        self.assertDictEqual(i.variables, {'Spike': [TOKEN_TYPES.STRING, "cake"]})

    def test_change_value(self):
        text = '''Did you know that Spike likes the number 12!
                  Now Spike likes 7:)'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {'Spike': [TOKEN_TYPES.NUM, 7]})

    def test_simple_addition(self):
        text = '''Did you know that Spike's age was the number 4!
                  I would add 2 to Spike's age!'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {"Spike's age": [TOKEN_TYPES.NUM, 6]})
    
    def test_addition_two_variables(self):
        text = '''Did you know that Spike's age was the number 4!
                  Did you know that Rarity's age was the number 15!
                  I would add Rarity's age to Spike's age!'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {"Spike's age": [TOKEN_TYPES.NUM, 19], "Rarity's age": [TOKEN_TYPES.NUM, 15]})

    def test_addition_strings(self):
        text = '''Did you know that Spike likes the word blue!
                  Did you know that Rarity likes the word berry!
                  I would add Rarity to Spike!'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {"Spike": [TOKEN_TYPES.STRING, "blueberry"], "Rarity": [TOKEN_TYPES.STRING, "berry"]})

    def test_cyrcle(self):
        text = '''Did you know that the sum was the number 0?
                  Did you know that Applejack's cake is the number 5?
                  As long as the sum was less than 3:
                  I would add 2 to Applejack's cake.
                  I would add 1 to the sum.
                  That's what I did.'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {"Applejack's cake": [TOKEN_TYPES.NUM, 11], "the sum": [TOKEN_TYPES.NUM, 3]})

    def test_if(self):
        text = '''Did you know that Spike's eaten cakes was the number 20?
                  Did you know that Twilight's reaction is the word Hello?
                    If Spike's eaten cakes was less than 2 then:
                    Now Twilight's reaction is Do you want one more?
                    Otherwise: If Spike's eaten cakes was less than 5 then:
                    Now Twilight's reaction is Okey.
                    Otherwise:
                    Now Twilight's reaction is AAAAAAAAAA!!!
                    That's what I would do!!!'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {"Twilight's reaction": [TOKEN_TYPES.STRING, "AAAAAAAAAA"], "Spike's eaten cakes": [TOKEN_TYPES.NUM, 20]})

    def test_input(self):
        io = IOTest()
        text = '''Did you know that Spike was the number!
                  Did you know that Applejack was the word!
                  I heard Spike!
                  I read Applejack!'''
        i = Interpretator(text, io)
        i.execute()
        self.assertEqual(i.io.value_print, "")
        self.assertDictEqual(i.variables, {'Spike': [TOKEN_TYPES.NUM, 123], "Applejack": [TOKEN_TYPES.STRING, "cakes"], })

    def test_output(self):
        io = IOTest()
        text = '''I said "Hello World"!
                  I wrote "8800"!
                  I sang "I want pass python exam!"!
                  I thought "It would be good"!'''
        i = Interpretator(text, io)
        i.execute()
        self.assertEqual(i.io.value_print, "Hello World\n8800\nI want pass python exam!\nIt would be good\n")
        self.assertDictEqual(i.variables, {})

    def test_ask(self):
        io = IOTest()
        text = '''Did you know that Spike was the number!
                  I asked Spike "How many gems are left?".
                  Did you know that Rarity was the word?
                  I asked Rarity "What is you favorite cake?".'''
        i = Interpretator(text, io)
        i.execute()
        self.assertEqual(i.io.value_print, "How many gems are left?\nWhat is you favorite cake?\n")
        self.assertDictEqual(i.variables, {'Spike': [TOKEN_TYPES.NUM, 123], 'Rarity': [TOKEN_TYPES.STRING, "cakes"]})


if __name__ == '__main__':
    unittest.main()
