import argparse

# import postgresql

from mssql_queries import MssqlToRam
from ram_to_pg_ddl import RamToPgDdl

if __name__ == "__main__":
    program = 'DataBaseConverter'
    description = """Программа для генерации DDL для PostgreSQL на основе базы данных Northwind."""

    argparser = argparse.ArgumentParser(prog=program, description=description)
    argparser.add_argument('-ddl', type=str, help='Путь к результирующему файлу DDL')

    arguments = argparser.parse_args()
    ddl_path = arguments.ddl  # Путь где сохрянятся DDL инструкции

    mssql = MssqlToRam('Driver={ODBC Driver 13 for SQL Server};Server=localhost\SQLEXPRESS;Database=Northwind;Trusted_Connection=yes;')
    schemas = mssql.load_data()

    ddl_generator = RamToPgDdl(schemas[1])
    ddls = ddl_generator.generate()
    ddl_generator.write_to_file(ddl_path)
    print("DDL: " + ddl_path)

    # conn = postgresql.open("pq://postgres:123@localhost:5432")
    # conn.execute('DROP DATABASE IF EXISTS northwindtest;')
    # conn.execute('CREATE DATABASE northwindtest;')
    # conn = postgresql.open("pq://postgres:123@localhost:5432/northwindtest")
    # conn.execute(ddls)
    # conn.close()