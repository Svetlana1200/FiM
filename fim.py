import sys
import os
from interpretator import Interpretator
from toJava import ToJava
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument ('file_name', nargs='?', help='Имя файла, в котором написан код на fim++')
    parser.add_argument ('--to-java', help='Имя файла, в котором написан код на fim++')
    namespace = parser.parse_args(sys.argv[1:])
    try:
        if namespace.file_name:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programs",  namespace.file_name)
            with open(path, 'r') as f:
                text = f.read().rstrip()
        else:
            text = sys.stdin.read().rstrip()
    except Exception:
        print("Не удается найти указанный файл.")
        sys.exit(1)
    except PermissionError:
        print("Не удается прочитать указанный файл.")
        sys.exit(1)
    
    if namespace.to_java:
        j = ToJava(text)
        j.translate()
        java_text = j.correct_text().replace('public class Program', f'public class {namespace.to_java[:-5]}')
        try:
            with open(namespace.to_java, 'w') as f:
                f.write(java_text)
        except (Exception, PermissionError):
            print("Не удается прочитать указанный файл.")
            sys.exit(1)
    else:
        i = Interpretator(text)
        i.execute()

    #print(i.variables)
    #print(i.method)
    #print(i.classes)


if __name__ == "__main__":
    main()
