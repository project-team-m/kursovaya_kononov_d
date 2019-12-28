'''В этом файле написан скелет для работы с директориями и файлами внутри
Так же именно здесь происходит конвертация кодировок файлов'''

import os
import re
from chardet.universaldetector import UniversalDetector


# Класс, который представляет из себя объект файла
class File:
    # Конструктор, в котором инициализируется файл
    def __init__(self, file_name, path='.'):
        self.file_name = file_name
        self.path = path

        # Узнаём кодировку файла
        detector = UniversalDetector()
        with open('{}/{}'.format(self.path, self.file_name), 'rb') as lines:
            for line in lines:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()

        self.encoding = detector.result['encoding']

    # Если это текстовый файл, который можно открыть, то вызываем конструктор.
    def __new__(cls, file_name, path='.'):
        try:
            open('{}/{}'.format(path, file_name), 'rb')
            return object.__new__(cls)
        except:
            return None

    def write(self, text):
        with open('{}/{}'.format(self.path, self.file_name), 'wb') as F:
            F.write(text)

    # Возвращает содержимое файла в байтах.
    def __str__(self):
        string = b''
        with open('{}/{}'.format(self.path, self.file_name), 'rb') as lines:
            for line in lines:
                string = string + line

        return string


# Класс, который представляет из себя дирректорию
class Dir:
    # Инициализация каталога и файлов внутри
    def __init__(self, path):
        if path == '':
            path = '.'
        self.__path = path
        self.all_files = os.listdir(path)
        # Массив элементов класса File
        self.__files = []
        for file in self.all_files:
            if re.search(r'.txt\b', file):
                tmp = File(file, path)
                if tmp:
                    self.__files.append(tmp)

    # Если дирректория существует, то вызываем конструктор
    def __new__(cls, path):
        try:
            return object.__new__(cls)
        except:
            return None

    # Возвращает файл, с возможностью изменения кодировки
    def show(self, ind):
        try:
            return self.__files[ind]
        except:
            return None

    # Возвращает массив имен файлов, в которых можно поменять кодировку
    def get_files(self):
        mass = []
        for i in self.__files:
            mass.append(i.file_name)
        return mass

    # Выводит все файлы в дирректории
    def show_all_files(self):
        if self.__path == '.':
            path = 'текущей дирректории'
        else:
            path = 'дирректории {}'.format(self.__path)
        s = 'Объекты в {}:'.format(path)
        if self.all_files:
            for i in self.all_files:
                s = '{} {}'.format(s, i)
        else:
            s = '{} {}'.format(s, 'Пусто')
        return s

    # Выводит все файлы в дирректории, в которых можно поменять кодировку.
    def __str__(self):
        if self.__path == '.':
            path = 'текущей дирректории'
        else:
            path = 'дирректории {}'.format(self.__path)
        s = 'Файлы с возможностью изменения кодировки в {}:'.format(path)
        if self.__files:
            for i in self.__files:
                s = '{} {}'.format(s, i.file_name)
        else:
            s = '{} {}'.format(s, 'Пусто')
        return s


# Класс для конвертации кодировок
class Convert:
    # Массив кодировок, с которыми работает программа
    encodings = [
        'utf-8',
        'utf-16',
        'utf-32',
        'windows-1251'
    ]

    # Статический метод для просмотра кодировки текста
    @staticmethod
    def show_encode(text):
        detector = UniversalDetector()
        detector.feed(text)
        detector.close()

        return detector.result['encoding']

    # Статический метод для конвертации текста
    @staticmethod
    def convert(text, encoding):
        try:
            text = text.decode(Convert.show_encode(text))
            text = text.encode(encoding)
            return text
        except:
            print('Неудача')
