'''В этом файле реализована возможность работы пользователя с программой через классы меню.'''

# Импортируем классы: Dir, File и Convert из views.py
from views import *


# Класс из которого будут наследоваться потомки всех меню
class Menu:
    # Статическая переменная для объекта с директорией
    dir = None

    # Конструктор, в котором инициализируется protected массив элементов меню с один элементом "Выход"
    def __init__(self):
        self._args = ['Выход']

    # Функция для работы с выбранными пунктами меню
    def case(self, arg):
        if arg == str(len(self._args)):
            return 1

    # Перегрузка операции len() для того, чтобы при написании len(object_Menu) возращалась длина массива элементов меню
    def __len__(self):
        return len(self._args)

    # Возращает строку для вывода его на экран
    def __str__(self):
        s = '1) {}'.format(self._args[0])
        for i in range(1, len(self._args)):
            s = '{}\n{}) {}'.format(s, i + 1, self._args[i])

        return '{}\n{}'.format(s, 'Выберете пункт: ')


# Это меню используется, если пользователь указал неверный путь. Класс наследуется от Menu
class RepeatDirMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self._args = [
            'Указать путь ещё раз.',
            self._args[-1]
        ]

    # Дополняем функцию case из класса Menu
    def case(self, arg):
        if arg == '1':
            return arg
        return Menu.case(self, arg)


# Меню для вывода содержимого файла
class PrintFile(Menu):
    def __init__(self):
        Menu.__init__(self)
        # Если пользователь указал путь до директории, то в меню будет выбор из этих файлов
        if Menu.dir:
            mass = Menu.dir.get_files()
        else:
            mass = []

        self._args = mass + [
            'Указать путь до нового файла.',
            self._args[-1]
        ]

    # Дополняем функцию case из класса Menu
    def case(self, arg):
        if arg == str(len(self._args) - 1):
            path = input('Укажите путь до файла: ')

            if len(path.split('/')) == 1:
                tmp = File(path)
            else:
                tmp = File(path.split('/')[-1], path[:(-1 * len(path.split('/')[-1])) - 1])
            if tmp:
                # Если пользователь указал путь до существующего файла и его можно открыть,
                # то его содержимое будет выведено на экран
                print(tmp.__str__().decode(tmp.encoding))
            else:
                # Иначе вызывается меню для повтора или выхода из данного пункта
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
                # Если пользователь выбрал один из файлов, находящихся в директории, которую он указал ранее,
                # то будет выведен этот файл
                print(Menu.dir.show(int(arg) - 1).__str__().decode(Menu.dir.show(int(arg) - 1).encoding))
            except:
                print('Неверно выбран пункт.')

        return Menu.case(self, arg)


# Меню для вывода кодировки файла, наследуется из Класса PrintFile,
# т.к. там конструктор выполняет необходимые нам функции
class PrintCodeFile(PrintFile):
    def __init__(self):
        PrintFile.__init__(self)

    # Переопределяем функцию case из класса Menu
    def case(self, arg):
        if arg == str(len(self._args) - 1):
            path = input('Укажите путь до файла: ')

            if len(path.split('/')) == 1:
                tmp = File(path)
            else:
                tmp = File(path.split('/')[-1], path[:(-1 * len(path.split('/')[-1])) - 1])
            if tmp:
                # Если пользователь указал путь до файла, который можно открыть, то будет выведена его кодировка
                print('Кодировка файла {} {}'.format(tmp.file_name, tmp.encoding))
            else:
                # Иначе будет предложена возможность ввести путь заново или выйти в главное меню
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
                # Если пользователь выбрал один из файлов, находящихся в директории, которую он указал ранее,
                # то будет выведена кодировка этого файла
                print('Кодировка файла {} {}'.format(Menu.dir.show(int(arg) - 1).file_name,
                                                     Menu.dir.show(int(arg) - 1).encoding))
            except:
                print('Неверно выбран пункт.')

        return Menu.case(self, arg)


# Класс для вывода всех поддерживаемых программой кодировок
class PrintEncodings(Menu):
    def __init__(self):
        Menu.__init__(self)
        # Переопределяет переменную с аргументами меню из класса Menu
        self._args = Convert.encodings + [
            'Отмена'
        ]

    # Дополняем функцию case из класса Menu
    def case(self, arg):
        try:
            # Если пользователь выбрал одну из предложенных кодировок, то функция вернет ещё название
            if int(arg) != len(self._args):
                return self._args[int(arg) - 1]
            else:
                Menu.case(self, arg)
        except:
            print('Неверно выбран пункт.')


# Меню в котором происходит изменение кодировки файла
class ChangeEncoding(PrintFile):
    def __init__(self):
        PrintFile.__init__(self)

    # Дополняем функцию case из класса Menu
    def case(self, arg):
        if arg == str(len(self._args) - 1):
            path = input('Укажите путь до файла: ')

            if len(path.split('/')) == 1:
                tmp = File(path)
            else:
                tmp = File(path.split('/')[-1], path[:(-1 * len(path.split('/')[-1])) - 1])
            if tmp:
                # Если пользователь указал корректный путь до файла, то ему будет предложен выбор кодировки,
                # в которую можно перекодировать файл
                Now_menu = PrintEncodings()
                while True:
                    print('Для файла {} с кодировкой {} выберете новую кодировку из списка'.format(tmp.file_name,
                                                                                                   tmp.encoding))
                    print(Now_menu)
                    switch = Now_menu.case(input())
                    if switch:
                        if switch != 1:
                            # После выбора кодировки записываем в файл содержимое в новой кодировке
                            tmp.write(Convert.convert(tmp.__str__(), switch))
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
                # То же самое, что и для файла, который пользователь указал по пути, за исключением того,
                # что берётся файл класса Dir из массива файлов класса Files
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
                                                                              switch))
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

    # Дополняем функцию case из класса Menu
    def case(self, arg):
        if arg == '1':
            path = input('Введите дирректорию, для выбора текущего каталога нажмите enter: ')
            try:
                # Создаём объект класса Dir, по пути, который указал пользователь
                Menu.dir = Dir(path)
                print('Успешно')
            except:
                # Если не удалось, то даём пользователю возмодность указать ещё раз или выйти назад.
                print('Неудача')
                Now_menu = RepeatDirMenu()
                while True:
                    print(Now_menu)
                    switch = Now_menu.case(input())
                    if switch == arg:
                        self.case(arg)
                        break
                    elif switch:
                        break
        elif arg == '2':
            # Выводит содержимое файла
            Now_menu = PrintFile()
            while True:
                print(Now_menu)
                if Now_menu.case(input()):
                    break
        elif arg == '3':
            # Выводит кодировку файла
            Now_menu = PrintCodeFile()
            while True:
                print(Now_menu)
                if Now_menu.case(input()):
                    break
        elif arg == '4':
            # Выводит лист всех файлов и папок в директории, которую указал пользователь
            if Menu.dir:
                print(Menu.dir.show_all_files())
            else:
                print('Директория пуста или не выбрана.')
        elif arg == '5':
            # Выводит названия всех файлов, в которых можно изменить кодировку, по пути, что указал пользователь
            if Menu.dir:
                print(Menu.dir)
            else:
                print('Директория пуста или не выбрана.')
        elif arg == '6':
            # Изменяет кодировку файла
            Now_menu = ChangeEncoding()
            while True:
                print(Now_menu)
                if Now_menu.case(input()):
                    break

        return Menu.case(self, arg)

    # Дополяем вывод на экран, для возможности выбора пункта меню
    def __str__(self):
        while True:
            print(Menu.__str__(self))
            if self.case(input()):
                break

        return 'Выход из программы'


# Точка входа
if __name__ == '__main__':
    a = MainMenu()
    print(a)