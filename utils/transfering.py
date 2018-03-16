# import postgresql
import logging
from datetime import datetime
import psycopg2
import pyodbc

from common.const import *
class DataTransfering:



    def __init__(self, db_name, user, pwd, mssql_url,logger_path):
        self.db_name = db_name
        # self.pg_server = pg_url
        self.mssql_server = mssql_url
        self.mssql_con = pyodbc.connect(self.mssql_server)
        # self.pg_con = postgresql.open(self.pg_server)
        self.pg_con = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(db_name,user,pwd))
        self.cursor = self.mssql_con.cursor()
        self.pg_cur = self.pg_con.cursor()
        self.df = "%Y.%m.%d %H:%M:%S"
        log_fh = open(logger_path, "w", encoding="utf-8")
        logging.basicConfig(filename=logger_path, level=logging.DEBUG)
        self.log = logging.getLogger("DataTransfering")

        logging._defaultFormatter = logging.Formatter("%(message)s")
        ch = logging.StreamHandler(log_fh)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(msecs)d-%(name)s-%(levelname)s: %(message)s')
        formatter.default_msec_format = '%s.%03d'
        formatter.datefmt="%d.%m.%Y %H:%M:%S"
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

    def start(self,schema):
        

        self.log.info("Старт переноса данных")

        start_time = datetime.now()
        self.pg_cur.execute('BEGIN TRANSACTION;')

        self.pg_cur.execute('SET CONSTRAINTS ALL DEFERRED;')
        for table in schema.tables:
            self.log.info("Начата обработка таблицы {}".format(table.name))

            self.cursor.execute('BEGIN TRANSACTION;')
            self.pg_cur.execute("ALTER TABLE {}.\"{}\" DISABLE TRIGGER ALL;\n".format(schema.name, table.name))
            self.cursor.execute(self.select_query(schema, table))
            count = 0
            batch = self.cursor.fetchmany(COUNT_FETCH_ROWS)
            while len(batch) > 0:
                count+=len(batch)
                self.log.debug("Старт транзакции загрузки фрагмента размера {}"
                              .format(len(batch)))

                batch_query = 'BEGIN TRANSACTION;\n'
                for row in batch:
                    batch_query += self.insert_query(schema, table, row) + ";\n"
                self.pg_cur.execute(batch_query)
                batch_query += 'COMMIT TRANSACTION;\n'
                self.log.debug("Финиш транзакции загрузки фрагмента"
                              .format(datetime.now().strftime(self.df)))
                batch = self.cursor.fetchmany(COUNT_FETCH_ROWS)

            self.pg_cur.execute("ALTER TABLE {}.\"{}\" ENABLE TRIGGER ALL;\n".format(schema.name, table.name))
            self.cursor.execute('COMMIT;')
            self.log.info("Записей добавлено: {}"
                          .format(count))
        self.pg_cur.execute('COMMIT TRANSACTION;')
        end_time = datetime.now()
        diff = end_time - start_time
        days, hours, minutes, seconds = self.convert_to_d_h_m_s(diff.total_seconds())
        mess = "Время выполнения переноса данных: {0}д, {1}ч, {2}м, {3}с".format(days, hours, minutes, seconds)
        self.log.info(mess)

    def cut(self, val, s):
        if int(val)>0:
            return '{0:.0f}{1} '.format(val,s)
        else:
            return ''

    def convert_to_d_h_m_s(self,seconds):

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        return int(days), int(hours), int(minutes), int(seconds)


    def select_query(self,schema,table):
        fields = []
        for field in table.fields:
            _str = '['+field.name+']'
            fields.append(_str)
        ss = ','.join(fields)
        query = 'SELECT {0} FROM [{1}].[{2}]'.format(ss,schema.name,table.name)
        # print(query)
        return query

    def insert_query(self,schema, table, values):
        fields = []

        for field in table.fields:
            fields.append(field.name)
        _values = []
        for value in values:
            val = str(value).replace('\'','') if value is not None else 'NULL'
            if val=='NULL':
                _values.append(val)
            else:
                _values.append('\'{}\''.format(val))
        query = 'INSERT INTO {}."{}" ({}) VALUES ({})' \
            .format(schema.name, table.name,', '.join(fields),', '.join(_values))

        return query