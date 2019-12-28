import os
import sys
import unittest


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from toJava import Translator
from symbolAndCommand import TOKEN_TYPES


class TranslatorTests(unittest.TestCase):
    def test_appropriation_number(self):
        text = '''Did you know that Spike was the number 12!'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), "var Spike = 12;")

    def test_appropriation_variable(self):
        text = '''Did you know that Spike was the number 12?
                Did you know that Rarity is the number?
                Now Rarity is Spike.'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), "var Spike = 12;\nint Rarity;\nRarity = Spike;")
    
    def test_words(self):
        text = '''Did you know that Spike likes the word cake?'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), 'var Spike = "cake";')

    def test_change_value(self):
        text = '''Did you know that Spike likes the number 12!
                  Now Spike likes 7:)'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), "var Spike = 12;\nSpike = 7;")

    def test_simple_addition(self):
        text = '''Did you know that Spike's age was the number 4!
                  I would add 2 to Spike's age!'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), "var Spike_s_age = 4;\nSpike_s_age += 2;")
    
    def test_addition_two_variables(self):
        text = '''Did you know that Spike's age was the number 4!
                  Did you know that Rarity's age was the number 15!
                  I would add Rarity's age to Spike's age!'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), "var Spike_s_age = 4;\nvar Rarity_s_age = 15;\nSpike_s_age += Rarity_s_age;")
    
    def test_addition_strings(self):
        text = '''Did you know that Spike likes the word blue!
                  Did you know that Rarity likes the word berry!
                  I would add Rarity to Spike!'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), 'var Spike = "blue";\nvar Rarity = "berry";\nSpike += Rarity;')
    

    def test_cyrcle(self):
        text = '''Did you know that the sum was the number 0?
                  Did you know that Applejack's cake is the number 5?
                  As long as the sum was less than 3:
                  I would add 2 to Applejack's cake.
                  I would add 1 to the sum.
                  That's what I did.'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), "var the_sum = 0;\nvar Applejack_s_cake = 5;\nwhile (the_sum < 3) {\nApplejack_s_cake += 2;\nthe_sum += 1;\n}")
    

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
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), ('var Spike_s_eaten_cakes = 20;\nvar Twilight_s_reaction = "Hello";\n' + 
                                            'if (Spike_s_eaten_cakes < 2) {\nTwilight_s_reaction = ' + 
                                            '"Do you want one more";\n}\nelse if (Spike_s_eaten_cakes < 5) ' + 
                                            '{\nTwilight_s_reaction = "Okey";\n}\nelse {\nTwilight_s_reaction = "AAAAAAAAAA";\n}'))
    
    def test_input(self):
        text = '''Did you know that Spike was the number!
                  Did you know that Applejack was the word!
                  I heard Spike!
                  I read Applejack!'''
        j = Translator(text, "Program")
        j.translate()
        self.assertEqual(j.correct_text(), 'int Spike;\nvar Applejack = "";\nScanner in = new Scanner(System.in);\nSpike = in.nextInt();\nApplejack = in.next();')
    
    def test_output(self):
        text = '''I said "Hello World"!
                  I wrote "8800"!
                  I sang "I want pass python exam!"!
                  I thought "It would be good"!'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), 'System.out.println("Hello World");\nSystem.out.println("8800");\nSystem.out.println("I want pass python exam!");\nSystem.out.println("It would be good");')
    
    def test_ask(self):
        text = '''Did you know that Spike was the number!
                  I asked Spike "How many gems are left?".'''
        j = Translator(text, "Program")
        j.translate() 
        self.assertEqual(j.correct_text(), 'int Spike;\nSystem.out.println("How many gems are left?");\nScanner in = new Scanner(System.in);\nSpike = in.nextInt();')
    

if __name__ == '__main__':
    unittest.main()
