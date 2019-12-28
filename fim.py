import sys
import os
from interpretator import Interpretator
from toJava import Translator
import argparse
import traceback


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument ('file_name', nargs='?', help='Имя файла, в котором написан код на fim++')
    parser.add_argument ('--to-java', help='Имя файла, в котором написан код на fim++')
    namespace = parser.parse_args(sys.argv[1:])
    try:
        if namespace.file_name:
            path = namespace.file_name
            with open(path, 'r') as f:
                text = f.read().rstrip()
        else:
            text = sys.stdin.read().rstrip()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        sys.exit(1)
    
    if namespace.to_java:
        j = Translator(text, os.path.splitext(namespace.to_java)[0])
        j.translate()
        java_text = j.correct_text()
        print(java_text)
        try:
            with open(namespace.to_java, 'w') as f:
                f.write(java_text)
        except Exception:
            print('Ошибка:\n', traceback.format_exc())
            sys.exit(1)
    else:
        i = Interpretator(text)
        i.execute()

    #print(i.variables)
    #print(i.method)
    #print(i.classes)


if __name__ == "__main__":
    main()
