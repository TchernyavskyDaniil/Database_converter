import argparse
import postgresql
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
    argparser.add_argument('-pg_url', type=str, help='URL подсключения к Postgresql базе', default="pq://postgres:123@localhost:5432")
    argparser.add_argument('-mssql_url', type=str, help='URL подсключения к MSSQL базе', default='Driver={ODBC Driver 13 for SQL Server};Server=localhost\SQLEXPRESS;Database=Northwind;Trusted_Connection=yes;')
    argparser.add_argument('-db_name', type=str, help='Имя postgres базы', default="northwindtest")

    arguments = argparser.parse_args()
    ddl_path = arguments.ddl  # Путь где сохрянятся DDL инструкции
    mssql_url = arguments.mssql_url
    pg_url = arguments.pg_url
    db_name = arguments.db_name
    xml_path = arguments.xml

    mssql = MssqlToRam(mssql_url)
    schemas = mssql.load('dbo')

    xdb_generator = RamToXdb(xml_path, schemas)
    xdb_generator.generate()
    print("XML: " + ddl_path)

    ddl_generator = RamToPgDdl(schemas)
    ddls = ddl_generator.generate(True)
    ddl_generator.write_to_file(ddl_path)
    print("DDL: " + ddl_path)

    conn = postgresql.open(pg_url)
    conn.execute('DROP DATABASE IF EXISTS {};'.format(db_name))
    conn.execute('CREATE DATABASE {};'.format(db_name))
    conn = postgresql.open("{}/{}".format(pg_url,db_name))
    conn.execute(ddls)
    conn.close()

    transfering = DataTransfering(db_name, "{}/{}".format(pg_url,db_name), mssql_url)
    transfering.start(schemas)
    print("Finish")