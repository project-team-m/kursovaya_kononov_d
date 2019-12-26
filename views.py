import os
import re
from chardet.universaldetector import UniversalDetector


class File:
    def __init__(self, file_name):
        self.file_name = file_name

        detector = UniversalDetector()
        with open(self.file_name, 'rb') as lines:
            for line in lines:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()

        self.encoding = detector.result['encoding']

    def __new__(cls, file_name):
        try:
            open(file_name, 'rb')
            return object.__new__(cls)
        except:
            return None

    def write(self, text):
        with open(self.file_name, 'wb') as F:
            F.write(text)

    def __str__(self):
        string = b''
        with open(self.file_name, 'rb') as lines:
            for line in lines:
                string = string + line

        return string


class Dir:
    def __init__(self, path):
        if path == '':
            path = '.'
        self.path = path
        self.all_files = os.listdir(path)
        self.__files = []
        for file in self.all_files:
            if re.search(r'.txt\b', file):
                tmp = File(file)
                if tmp:
                    self.__files.append(tmp)

    def __new__(cls, path):
        try:
            return object.__new__(cls)
        except:
            return None

    def show(self, ind):
        try:
            return self.__files[ind]
        except:
            return None

    def show_all_files(self):
        if self.path == '.':
            path = 'текущей дирректории'
        else:
            path = 'дирректории {}'.format(self.path)
        s = 'Файлы в {}:'.format(path)
        if self.all_files:
            for i in self.all_files:
                s = '{} {}'.format(s, i)
        else:
            s = '{} {}'.format(s, 'Пусто')
        return s

    def __str__(self):
        if self.path == '.':
            path = 'текущей дирректории'
        else:
            path = 'дирректории {}'.format(self.path)
        s = 'Файлы с возможностью изменения кодировки в {}:'.format(path)
        if self.__files:
            for i in self.__files:
                s = '{} {}'.format(s, i.file_name)
        else:
            s = '{} {}'.format(s, 'Пусто')
        return s


class Convert:
    def __init__(self):
        self.encodings = [
            'utf-8',
            'utf-16',
            'utf-32',
            'windows-1251'
        ]

    @staticmethod
    def show_encode(text):
        detector = UniversalDetector()
        detector.feed(text)
        detector.close()

        return detector.result['encoding']

    @staticmethod
    def convert(text, encoding, encoding_was):
        text = text.decode(encoding_was)
        text = text.encode(encoding)
        return text


if __name__ == '__main__':
    a = Dir('')
    b = Convert()
    c = File('test.txt')
    print(b.show_encode(c.__str__()))
    c.write(b.convert(c.__str__(), b.encodings[1], c.encoding))
