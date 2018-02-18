import argparse
from dbd_to_ram import DbdToRam
from ram_to_pg_ddl import RamToPgDdl
# import postgresql


if __name__ == "__main__":
    program = 'DataBaseConverter'
    description = """Программа для генерации DDL для PostgreSQL на основе DBD-описателя."""

    argparser = argparse.ArgumentParser(prog=program, description=description)
    argparser.add_argument('-f', type=str, help='Файл базы данных')
    argparser.add_argument('-ddl', type=str, help='Путь к результирующему файлу DDL')

    arguments = argparser.parse_args()

    dbd_file = arguments.f  # DBD-файл, поданый на вход
    ddl_path = arguments.ddl  # Путь где сохрянятся DDL инструкции

    dbd_parser = DbdToRam(dbd_file)

    ram = dbd_parser.parse()

    ddl_generator = RamToPgDdl(ram)
    ddls = ddl_generator.generate()
    ddl_generator.write_to_file(ddl_path)
    print("DDL: " + ddl_path)
    print("Finished")

    # conn = postgresql.open("pq://postgres:123@localhost:5432")
    # conn.execute('DROP DATABASE IF EXISTS test;')
    # conn.execute('CREATE DATABASE test;')
    # conn = postgresql.open("pq://postgres:123@localhost:5432/test")
    #
    # conn.execute(ddls)

    # print(ddls)

    # conn.close()


