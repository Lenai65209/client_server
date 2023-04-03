import locale
import subprocess

from chardet.universaldetector import UniversalDetector

# 1 Каждое из слов «разработка», «сокет», «декоратор» представить в
# строковом формате и проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление в
# формат Unicode и также проверить тип и содержимое переменных.

st_dev = ['разработка', 'сокет', 'декоратор']
for el in st_dev:
    print(el)
    print(type(el))

st_dev = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
          '\u0441\u043e\u043a\u0435\u0442',
          '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']
for el in st_dev:
    print(el)
    print(type(el))

# 2 Каждое из слов «class», «function», «method» записать в байтовом типе без
# преобразования в последовательность кодов (не используя методы encode и
# decode) и определить тип, содержимое и длину соответствующих переменных

st_dev = [b'class', b'function', b'method']
for el in st_dev:
    print(el)
    print(type(el))
    print(len(el))

# 3 Определить, какие из слов «attribute», «класс», «функция», «type»
# невозможно записать в байтовом типе.
# 'класс', 'функция' невозможно записать в байтовом типе.

st_dev = ['attribute', 'класс', 'функция', 'type']
for el in st_dev:
    el_enc = el.encode('ascii', 'ignore')
    print(el_enc)
    print(type(el_enc))

# 4 Преобразовать слова «разработка», «администрирование», «protocol»,
# «standard» из строкового представления в байтовое и выполнить обратное
# преобразование (используя методы encode и decode).

st_dev = ['разработка', 'администрирование', '«protocol', 'standard']
for el in st_dev:
    el_enc = el.encode('ascii', 'ignore')
    print(ascii(el_enc))
    print(type(el_enc))
    el_dec = el_enc.decode('ascii', 'ignore')
    print(ascii(el_dec))
    print(type(el_dec))

# 5 Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
# результаты из байтовового в строковый тип на кириллице.

# import subprocess

# from chardet.universaldetector import UniversalDetector

detector = UniversalDetector()

args = ['ping', 'youtube.com']
subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in subproc_ping.stdout:
    # print(line.decode('cp866').encode('utf-8').decode('utf-8'))
    detector.feed(line)
    detector.close()
    cod = detector.result['encoding']
    print(cod)
    print(line.decode(cod).encode('utf-8').decode('utf-8'), end='')
    detector.reset()  # сбрасываем детектор в исходное состояние

args = ['ping', 'yandex.ru']
subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in subproc_ping.stdout:
    # print(line.decode('cp866').encode('utf-8').decode('utf-8'))
    detector.feed(line)
    detector.close()
    cod = detector.result['encoding']
    print(cod)
    print(line.decode(cod).encode('utf-8').decode('utf-8'), end='')
    detector.reset()  # сбрасываем детектор в исходное состояние

# 6 Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор». Проверить кодировку файла
# по умолчанию. Принудительно открыть файл в формате Unicode и вывести его
# содержимое.

# import locale

# from chardet.universaldetector import UniversalDetector

detector = UniversalDetector()

with open('test_file.txt') as f_n:
    for el_str in f_n:
        print(el_str, end='')

def_coding = locale.getpreferredencoding()
print(def_coding)  # кодировка по умолчанию: cp1251

with open('test_file.txt', 'br') as f_n:
    for el_str in f_n:  # проходимся по строкам файла в режиме 'rb'
        detector.feed(el_str)
        detector.close()
        cod = detector.result['encoding']
        print(cod)
        print(el_str.decode(cod).encode('utf-8').decode('utf-8'), end='')
        detector.reset()  # сбрасываем детектор в исходное состояние

