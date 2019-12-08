FiM++
Автор: Семенова Светлана
Требования
	
Состав:
	Тесты: test_programs.py
	fim.py, interpretator.py, lexer.py, symbolAndCommand.py
	Тестовые программы: add_from_1_to_100.fimpp, calculator.fimpp, Drinking_Song.fimpp, factorial.fimpp,
				fibonacci.fimpp, gcd.fimpp, hello_world.fimpp
Пример запуска:
	./fim.py add_from_1_to_100.fimpp
	typo add_from_1_to_100.fimpp | fim.py (windows)
	cat add_from_1_to_100.fimpp | fim.py (linux)
	./fim.py add_from_1_to_100.fimpp --to-java adding.java
Дополнительно:
	Ввод программы на языке fim++ осуществляется через параметры запуска или через stdin.
	--to-java [Имя файла.java] для перевода программы на fim++ в программу на java, результат будет записан в указанный файл