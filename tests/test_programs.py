import os
import sys
import unittest


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from fim import Lexer, SymbolAndCommand, Interpretator, IOTest


class GameTest(unittest.TestCase):
    def test_appropriation(self):
        text = '''Did you know that Spike was the number 12!'''
        i = Interpretator(text)
        i.execute() 
        self.assertDictEqual(i.variables, {'Spike': [SymbolAndCommand.NUM, 12]})

    def test_words(self):
        text = '''Did you know that Spike likes the word cake?'''
        i = Interpretator(text)
        i.execute()    
        self.assertDictEqual(i.variables, {'Spike': [SymbolAndCommand.STRING, "cake"]})

    def test_change_value(self):
        text = '''Did you know that Spike likes the number 12!
                  Now Spike likes 7:)'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {'Spike': [SymbolAndCommand.NUM, 7]})

    def test_simple_addition(self):
        text = '''Did you know that Spike's age was the number 4!
                  I would add 2 to Spike's age!'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {"Spike's age": [SymbolAndCommand.NUM, 6]})
    
    def test_addition_two_variables(self):
        text = '''Did you know that Spike's age was the number 4!
                  Did you know that Rarity's age was the number 15!
                  I would add Rarity's age to Spike's age!'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {"Spike's age": [SymbolAndCommand.NUM, 19], "Rarity's age": [SymbolAndCommand.NUM, 15]})

    def test_addition_strings(self):
        text = '''Did you know that Spike likes the word blue!
                  Did you know that Rarity likes the word berry!
                  I would add Rarity to Spike!'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {"Spike": [SymbolAndCommand.STRING, "blueberry"], "Rarity": [SymbolAndCommand.STRING, "berry"]})

    def test_cyrcle(self):
        text = '''Did you know that the sum was the number 0?
                  Did you know that Applejack's cake is the number 5?
                  As long as the sum was less than 3:
                  I would add 2 to Applejack's cake.
                  I would add 1 to the sum.
                  That's what I did.'''
        i = Interpretator(text)
        i.execute()
        self.assertDictEqual(i.variables, {"Applejack's cake": [SymbolAndCommand.NUM, 11], "the sum": [SymbolAndCommand.NUM, 3]})

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
        self.assertDictEqual(i.variables, {"Twilight's reaction": [SymbolAndCommand.STRING, "AAAAAAAAAA"], "Spike's eaten cakes": [SymbolAndCommand.NUM, 20]})

    def test_input(self):
        io = IOTest()
        text = '''Did you know that Spike was the number!
                  Did you know that Applejack was the word!
                  I heard Spike!
                  I read Applejack!'''
        i = Interpretator(text, io)
        i.execute()
        self.assertEqual(i.io.value_print, "")
        self.assertDictEqual(i.variables, {'Spike': [SymbolAndCommand.NUM, 123], "Applejack": [SymbolAndCommand.STRING, "cakes"], })

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
        self.assertDictEqual(i.variables, {'Spike': [SymbolAndCommand.NUM, 123], 'Rarity': [SymbolAndCommand.STRING, "cakes"]})


if __name__ == '__main__':
    unittest.main()