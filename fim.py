import sys
import os
from interpretator import Interpretator
from toJava import ToJava

def main():
    try:
        if len(sys.argv) == 2:
            name_file = sys.argv[1]
            with open(name_file, 'r') as f:
                text = f.read().rstrip()
        else:
            text = sys.stdin.read().rstrip()
    except Exception:
        print("Не удается найти указанный файл.")
        sys.exit(1)

    #i = Interpretator(text)
    #i.execute()

    #print(i.variables)
    #print(i.method)
    #print(i.classes)
    
    j = ToJava(text)
    j.translate()
    j.correct_text()


if __name__ == "__main__":
    main()
