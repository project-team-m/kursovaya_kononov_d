import os
import re


class File:
    def __init__(self, file_name):
        self.file_name = file_name

    def __new__(cls, file_name):
        try:
            open(file_name, 'r')
            return object.__new__(cls)
        except:
            print('File {} is not exists'.format(file_name))
            return None

    def write(self, text):
        with open(self.file_name, 'w') as F:
            print('File: {}'.format(self.file_name))
            F.write(text)

    def __str__(self):
        with open(self.file_name, 'r') as lines:
            string = 'File: {}'.format(self.file_name)
            for line in lines:
                string = '{}{}'.format(string, line)

        return string


class Dir:
    def __init__(self, path):
        self.path = path
        self.all_files = os.listdir(path)
        self.files = []
        for file in self.all_files:
            if re.search(r'.txt\b', file):
                tmp = File(file)
                if tmp:
                    self.files.append(tmp)

    def __new__(cls, path):
        try:
            return object.__new__(cls)
        except:
            print('No such directory')
            return None

    def show(self, ind):
        try:
            return self.files[ind]
        except:
            return None

    def __str__(self):
        files = self.all_files[0]
        for file in self.all_files[1:]:
            files = '{}, {}'.format(files, file)
        return '{}\n{}'.format(self.path, files)


if __name__ == '__main__':
    a = Dir('/home/dekeyel/Projects/labs5sem/dima/oop/kurs')
    print(a.show(0))
