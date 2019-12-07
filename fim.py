import sys
import os
from interpretator import Interpretator
from toJava import ToJava

def main():
    '''try:
        if len(sys.argv) == 2:
            name_file = sys.argv[1]
            with open(name_file, 'r') as f:
                text = f.read().rstrip()
        else:
            text = sys.stdin.read().rstrip()
    except Exception:
        print("Не удается найти указанный файл.")
        sys.exit(1)

    i = Interpretator(text)
    i.execute()

    print(i.variables)
    print(i.method)
    print(i.classes)'''
    text = '''Dear Princess Celestia: Letter One.

Today I learned how to sing Applejack's Drinking Song.

Did you know that Applejack likes the number 99?

As long as Applejack had no less than 1:
	I sang Applejack" jugs of cider on the wall, "Applejack" jugs of cider,".
	I would subtract 1 from Applejack.

	If Applejack had more than 1:
		I sang "Take one down and pass it around, "Applejack" jugs of cider on the wall.".

	Otherwise: If Applejack had 1:
		I sang "Take one down and pass it around, 1 jug of cider on the wall. 1 jug of cider on the wall, 1 jug of cider. Take one down and pass it around, no more jugs of cider on the wall.".

	Otherwise:
		I sang "No more jugs of cider on the wall, no more jugs of cider.Go to the store and buy some more, 99 jugs of cider on the wall.".
	That's what I would do.
That's what I did.

That's all about how to sing Applejack's Drinking Song!

Your faithful student, Twilight Sparkle.'''   
    j = ToJava(text)
    j.translate()


if __name__ == "__main__":
    main()
