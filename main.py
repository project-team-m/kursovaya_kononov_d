from views import *


class Menu:
    dir = None

    def __init__(self):
        self._args = ['Выход']

    def case(self, arg):
        if arg == str(len(self._args)):
            return 1

    def __len__(self):
        return len(self._args)

    def __str__(self):
        s = '1) {}'.format(self._args[0])
        for i in range(1, len(self._args)):
            s = '{}\n{}) {}'.format(s, i + 1, self._args[i])

        return '{}\n{}'.format(s, 'Выберете пункт: ')


class RepeatDirMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self._args = [
            'Указать путь ещё раз.',
            self._args[-1]
        ]
        self.path = None

    def case(self, arg):
        if arg == '1':
            return arg
        return Menu.case(self, arg)


class PrintFile(Menu):
    def __init__(self):
        Menu.__init__(self)
        if Menu.dir:
            mass = Menu.dir.get_files()
        else:
            mass = []

        self._args = mass + [
            'Указать путь до нового файла.',
            self._args[-1]
        ]

    def case(self, arg):
        if arg == str(len(self._args) - 1):
            path = input('Укажите путь до файла: ')

            if len(path.split('/')) == 1:
                tmp = File(path)
            else:
                tmp = File(path.split('/')[-1], path[:(-1 * len(path.split('/')[-1])) - 1])
            if tmp:
                print(tmp.__str__().decode(tmp.encoding))
            else:
                print('Неудача')
                Now_menu = RepeatDirMenu()
                while True:
                    print(Now_menu)
                    switch = Now_menu.case(input())
                    if switch == '1':
                        self.case(arg)
                        break
                    elif switch:
                        break
        elif not Menu.case(self, arg):
            try:
                print(Menu.dir.show(int(arg) - 1))
            except:
                print('Неверно выбран пункт.')

        return Menu.case(self, arg)


class PrintCodeFile(PrintFile):
    def __init__(self):
        PrintFile.__init__(self)

    def case(self, arg):
        if arg == str(len(self._args) - 1):
            path = input('Укажите путь до файла: ')

            if len(path.split('/')) == 1:
                tmp = File(path)
            else:
                tmp = File(path.split('/')[-1], path[:(-1 * len(path.split('/')[-1])) - 1])
            if tmp:
                print('Кодировка файла {} {}'.format(tmp.file_name, tmp.encoding))
            else:
                print('Неудача')
                Now_menu = RepeatDirMenu()
                while True:
                    print(Now_menu)
                    switch = Now_menu.case(input())
                    if switch == '1':
                        self.case(arg)
                        break
                    elif switch:
                        break
        elif not Menu.case(self, arg):
            try:
                print('Кодировка файла {} {}'.format(Menu.dir.show(int(arg) - 1).file_name,
                                                     Menu.dir.show(int(arg) - 1).encoding))
            except:
                print('Неверно выбран пункт.')

        return Menu.case(self, arg)


class PrintEncodings(Menu):
    def __init__(self):
        Menu.__init__(self)
        self._args = Convert.encodings + [
            'Отмена'
        ]

    def case(self, arg):
        try:
            if int(arg) != len(self._args):
                return self._args[int(arg) - 1]
            else:
                Menu.case(self, arg)
        except:
            print('Неверно выбран пункт.')


class ChangeEncoding(PrintFile):
    def __init__(self):
        PrintFile.__init__(self)

    def case(self, arg):
        if arg == str(len(self._args) - 1):
            path = input('Укажите путь до файла: ')

            if len(path.split('/')) == 1:
                tmp = File(path)
            else:
                tmp = File(path.split('/')[-1], path[:(-1 * len(path.split('/')[-1])) - 1])
            if tmp:
                Now_menu = PrintEncodings()
                while True:
                    print('Для файла {} с кодировкой {} выберете новую кодировку из списка'.format(tmp.file_name,
                                                                                                   tmp.encoding))
                    print(Now_menu)
                    switch = Now_menu.case(input())
                    if switch:
                        if switch != 1:
                            tmp.write(Convert.convert(tmp.__str__(), switch, tmp.encoding))
                            break
                        else:
                            break

            else:
                print('Неудача')
                Now_menu = RepeatDirMenu()
                while True:
                    print(Now_menu)
                    switch = Now_menu.case(input())
                    if switch == '1':
                        self.case(arg)
                        break
                    elif switch:
                        break
        elif not Menu.case(self, arg):
            try:
                Now_menu = PrintEncodings()
                while True:
                    print('Для файла {} с кодировкой {} выберете новую кодировку из списка'.format(
                        Menu.dir.show(int(arg) - 1).file_name,
                        Menu.dir.show(int(arg) - 1).encoding)
                    )
                    print(Now_menu)
                    switch = Now_menu.case(input())
                    if switch:
                        if switch != 1:
                            Menu.dir.show(int(arg) - 1).write(Convert.convert(Menu.dir.show(int(arg) - 1).__str__(),
                                                                              switch,
                                                                              Menu.dir.show(int(arg) - 1).encoding))
                            break
                        else:
                            break
            except:
                print('Неверно выбран пункт.')

        return Menu.case(self, arg)


class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self._args = [
            'Выбрать дирректорию.',
            'Вывести содержание файла.',
            'Вывести кодировку файла.',
            'Вывести все файлы и папки в дирректории.',
            'Вывести файлы, с возможностью смены кодировки.',
            'Изменить кодировку файла.',
            self._args[-1]
        ]

    def case(self, arg):
        if arg == '1':
            path = input('Введите дирректорию, для выбора текущего каталога нажмите enter: ')
            try:
                Menu.dir = Dir(path)
                print('Успешно')
            except:
                print('Неудача')
                Now_menu = RepeatDirMenu()
                while True:
                    print(Now_menu)
                    switch = Now_menu.case(input())
                    print(switch)
                    if switch == arg:
                        self.case(arg)
                        break
                    elif switch:
                        break
        elif arg == '2':
            Now_menu = PrintFile()
            while True:
                print(Now_menu)
                if Now_menu.case(input()):
                    break
        elif arg == '3':
            Now_menu = PrintCodeFile()
            while True:
                print(Now_menu)
                if Now_menu.case(input()):
                    break
        elif arg == '4':
            if Menu.dir:
                print(Menu.dir.show_all_files())
            else:
                print('Директория пуста или не выбрана.')
        elif arg == '5':
            if Menu.dir:
                print(Menu.dir)
            else:
                print('Директория пуста или не выбрана.')
        elif arg == '6':
            Now_menu = ChangeEncoding()
            while True:
                print(Now_menu)
                if Now_menu.case(input()):
                    break

        return Menu.case(self, arg)

    def __str__(self):
        while True:
            print(Menu.__str__(self))
            if self.case(input()):
                break

        return 'Выход из программы'


a = MainMenu()
print(a)
