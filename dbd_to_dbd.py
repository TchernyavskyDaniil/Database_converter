import argparse
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from common.const import *
from utils.mssql_to_ram import MssqlToRam
from utils.ram_to_pg_ddl import RamToPgDdl
from utils.ram_to_xdb import RamToXdb
from utils.transfering import DataTransfering

if __name__ == "__main__":
    program = 'DataBaseConverter'
    description = """Программа для генерации DDL для PostgreSQL на основе базы данных MSSQL."""
    argparser = argparse.ArgumentParser(prog=program, description=description)
    argparser.add_argument('-ddl', type=str, help='Путь к результирующему файлу DDL')
    argparser.add_argument('-xml', type=str, help='Путь к результирующему файлу XML')
    argparser.add_argument("-pg_user", type=str, help='Пользователь Postgresql базы', default=DEFAULT_PG_USER)
    argparser.add_argument("-pg_pwd", type=str, help='Пароль Postgresql базы', default=DEFAULT_PG_USER_PWD)

    argparser.add_argument('-mssql_url', type=str, help='URL подсключения к MSSQL базе', default=MSSQL_CON_URL)
    argparser.add_argument('-db_name', type=str, help='Имя postgres базы', default=DEFAULT_MSSQL_DB)
    argparser.add_argument('-log', type=str, default=LOG_PATH)

    arguments = argparser.parse_args()
    ddl_path = arguments.ddl  # Путь где сохрянятся DDL инструкции
    mssql_url = arguments.mssql_url
    db_name = arguments.db_name
    xml_path = arguments.xml
    logger_path = arguments.log
    user = arguments.pg_user
    pwd = arguments.pg_pwd


    mssql = MssqlToRam(mssql_url)

    schemas = mssql.load('dbo')

    xdb_generator = RamToXdb(xml_path, schemas)
    xdb_generator.generate()
    print("XML: " + xml_path)

    ddl_generator = RamToPgDdl(schemas)
    ddls = ddl_generator.generate(True)
    ddl_generator.write_to_file(ddl_path)
    print("DDL: " + ddl_path)

    conn = psycopg2.connect("dbname='{}' user='{}' password='{}'".format('postgres', user, pwd))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute('DROP DATABASE IF EXISTS {};'.format(db_name))
    cur.execute('CREATE DATABASE {};'.format(db_name))
    conn = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(db_name, user, pwd))
    cur = conn.cursor()
    cur.execute('BEGIN TRANSACTION;')
    cur.execute(ddls)
    cur.execute('COMMIT;')

    conn.close()

    transfering = DataTransfering(db_name, user, pwd , mssql_url,logger_path)
    transfering.start(schemas)
    print("Finish")