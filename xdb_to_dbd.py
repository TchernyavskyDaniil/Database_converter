import argparse
from xdb_to_ram import XdbToRam
from ram_to_dbd import RamToDbd

# DOWNLOADING DATA FROM DBD TO XML



if __name__ == "__main__":
    program = 'DataBaseConverter'
    description = """Программа для преобразования XDB-описателя в DBD-описатель."""
    epilog = ''


    argparser = argparse.ArgumentParser(prog=program, description=description, epilog=epilog)
    argparser.add_argument('-f', '--file', type=str, default='source/tasks.xml',
                           help='Конвертирование XDB -> DBD. Результат - файл .db',
                           metavar='file.xml - файл XDB-описателя')

    arguments = argparser.parse_args()

    xdb_file = arguments.file  # XDB-файл, поданый на вход

    xdb_parser = XdbToRam(xdb_file)

    ram = xdb_parser.parse()

    dbd_generator = RamToDbd(xdb_file.replace('.xml', '.db'), ram)
    dbd_generator.generate()

    print("Finished")