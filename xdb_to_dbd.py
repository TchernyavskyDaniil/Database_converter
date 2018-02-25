import argparse

from utils.ram_to_dbd import RamToDbd
from utils.xdb_to_ram import XdbToRam

if __name__ == "__main__":
    program = 'DataBaseConverter'
    description = """Программа для преобразования XDB-описателя в DBD-описатель."""

    argparser = argparse.ArgumentParser(prog=program, description=description)
    argparser.add_argument('-f', '--file', type=str, default='source/tasks.xml',
                           help='Конвертирование XDB -> DBD. Результат - файл .db',
                           metavar='file.xml - файл XDB-описателя')
    argparser.add_argument('-db', type=str, default='source/test_db.db',
                           help='Конвертирование XDB -> DBD. Результат - файл .db',
                           metavar='db.db - результат работы программы')

    arguments = argparser.parse_args()

    xdb_file = arguments.file  # XDB-файл, поданый на вход
    db = arguments.db

    xdb_parser = XdbToRam(xdb_file)

    ram = xdb_parser.parse()

    dbd_generator = RamToDbd(db, ram)
    dbd_generator.generate()

    print("Finished")
