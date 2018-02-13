import argparse
from dbd_to_ram import DbdToRam
from ram_to_pg_ddl import RamToPgDdl
import postgresql


if __name__ == "__main__":
    program = 'DataBaseConverter'
    description = """Программа для генерации DDL для PostgreSQL на основе DBD-описателя."""
    epilog = ''

    argparser = argparse.ArgumentParser(prog=program, description=description, epilog=epilog)
    argparser.add_argument('-f', '--file', type=str, default='source/test_db1.db',
                           help='Конвертирование DBD -> DDL для PostgreSQL. Результат - файл .ddl',
                           metavar='file.db - файл DBD-описателя')

    arguments = argparser.parse_args()

    dbd_file = arguments.file  # DBD-файл, поданый на вход

    dbd_parser = DbdToRam(dbd_file)

    ram = dbd_parser.parse()

    ddl_generator = RamToPgDdl(dbd_file.replace('.db', '.ddl'), ram)
    ddls = ddl_generator.generate()

    conn = postgresql.open("pq://postgres:123@localhost:5432")
    conn.execute('DROP DATABASE IF EXISTS test;')
    conn.execute('CREATE DATABASE test;')
    conn = postgresql.open("pq://postgres:123@localhost:5432/test")

    conn.execute(ddls)

    print(ddls)

    conn.close()

    print("Finished")
