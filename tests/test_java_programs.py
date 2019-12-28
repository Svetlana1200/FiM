import os
import sys
import unittest


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from toJava import Translator


class TranslatorTests(unittest.TestCase):
    def test_add_from_1_to_100(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programs",  "add_from_1_to_100.fimpp")
        with open (path, 'r') as f:
            text = f.read()
        j = Translator(text, "add_from_1_to_100")
        j.translate() 
        java_code = j.correct_text()
    
    def test_calculator(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programs",  "calculator.fimpp")
        with open (path, 'r') as f:
            text = f.read()
        j = Translator(text, "calculator")
        j.translate() 
        java_code = j.correct_text()
    
    def test_Drinking_Song(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programs",  "Drinking_Song.fimpp")
        with open (path, 'r') as f:
            text = f.read()
        j = Translator(text, "Drinking_Song")
        j.translate() 
        java_code = j.correct_text()

    def test_factorial(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programs",  "factorial.fimpp")
        with open (path, 'r') as f:
            text = f.read()
        j = Translator(text, "factorial")
        j.translate() 
        java_code = j.correct_text()

    def test_fibonacci(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programs",  "fibonacci.fimpp")
        with open (path, 'r') as f:
            text = f.read()
        j = Translator(text, "fibonacci")
        j.translate() 
        java_code = j.correct_text()

    def test_gcd(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programs",  "gcd.fimpp")
        with open (path, 'r') as f:
            text = f.read()
        j = Translator(text, "gcd")
        j.translate() 
        java_code = j.correct_text()

    def test_hello_world(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programs",  "hello_world.fimpp")
        with open (path, 'r') as f:
            text = f.read()
        j = Translator(text, "hello_world")
        j.translate() 
        java_code = j.correct_text()
        
        
if __name__ == '__main__':
    unittest.main()
