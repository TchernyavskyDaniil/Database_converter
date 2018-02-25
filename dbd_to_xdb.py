import argparse

from utils.dbd_to_ram import DbdToRam
from utils.ram_to_xdb import RamToXdb

if __name__ == "__main__":
    program = 'DataBaseConverter'
    description = """Программа для преобразования DBD-описателя в XDB-описатель ."""
    epilog = ''

    argparser = argparse.ArgumentParser(prog=program, description=description, epilog=epilog)
    argparser.add_argument('-f', '--file', type=str, default='source/tasks1.xml',
                           help='Конвертирование XDB -> DBD. Результат - файл .db',
                           metavar='file.xml - результирующий файл XDB-описателя')
    argparser.add_argument('-db', type=str, default='source/test_db.db',
                           help='Конвертирование XDB -> DBD. Результат - файл .db',
                           metavar='db.db - файл бызй данных')

    arguments = argparser.parse_args()

    xdb_file = arguments.file  # XDB-файл, поданый на вход
    db = arguments.db

    dbd_parser = DbdToRam(db)

    ram = dbd_parser.parse()

    xdb_generator = RamToXdb(xdb_file,ram)
    xdb_generator.generate()

    print("Finished")
