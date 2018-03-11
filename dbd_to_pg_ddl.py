import argparse
import postgresql

from common.const import *
from utils.dbd_to_ram import DbdToRam
from utils.ram_to_pg_ddl import RamToPgDdl
from utils.xdb_to_ram import XdbToRam


if __name__ == "__main__":
    program = 'DataBaseConverter'
    description = """Программа для генерации пустой PostgreSQL быза на основе DBD - или XDB - описателя."""

    argparser = argparse.ArgumentParser(prog=program, description=description)
    argparser.add_argument('-db', type=str, help='Файл базы данных')
    argparser.add_argument('-xml', type=str, help='Файл xml представления метаданных')
    argparser.add_argument('-ddl', type=str, help='Путь к результирующему файлу DDL')
    argparser.add_argument('-url', type=str, help='URL подсключения к Postgresql базе', default=PG_CON_URL)
    argparser.add_argument('-db_name', type=str, help='Имя postgres базы', default=DEFAULT_PG_DB)

    arguments = argparser.parse_args()

    dbd_file = arguments.db         # DBD-файл, поданый на вход
    xml_file = arguments.xml        # XDB-файл, поданый на вход
    ddl_path = arguments.ddl        # Путь где сохрянятся DDL инструкции
    db_name = arguments.db_name     # Имя базы
    url = arguments.url             # URL для подключения к базе

    parser = None
    if dbd_file:
        parser = DbdToRam(dbd_file)
    elif xml_file:
        parser = XdbToRam(xml_file)
    else:
        print("Источник данных не указан")
        quit()

    ram = parser.parse()

    ddl_generator = RamToPgDdl(ram)
    ddls = ddl_generator.generate(False)
    ddl_generator.write_to_file(ddl_path)
    print("DDL: " + ddl_path)


    conn = postgresql.open(url)
    conn.execute('DROP DATABASE IF EXISTS {};'.format(db_name))
    conn.execute('CREATE DATABASE {};'.format(db_name))
    conn = postgresql.open("{}/{}".format(url,db_name))

    conn.execute(ddls)
    conn.close()

    print("Finished")

