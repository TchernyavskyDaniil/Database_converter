# import postgresql
import datetime
import psycopg2
import pyodbc

class DataTransfering:


    def __init__(self, db_name, user, pwd, mssql_url):
        self.db_name = db_name
        # self.pg_server = pg_url
        self.mssql_server = mssql_url
        self.mssql_con = pyodbc.connect(self.mssql_server)
        # self.pg_con = postgresql.open(self.pg_server)
        self.pg_con = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(db_name,user,pwd))
        self.cursor = self.mssql_con.cursor()
        self.pg_cur = self.pg_con.cursor()
        self.log = None
        self.df = "%Y.%m.%d %H:%M:%S"

    def start(self,schema, logger):
        self.log = logger
        self.log.info("[{}]:  Старт переноса данных".format(datetime.datetime.now().strftime(self.df)))

        start_time = datetime.datetime.now()

        self.pg_cur.execute('BEGIN TRANSACTION;')

        self.pg_cur.execute('SET CONSTRAINTS ALL DEFERRED;')
        for table in schema.tables:
            self.log.info(" ")
            self.log.info("[{}]:  Начата обработка таблицы {}"
                          .format(datetime.datetime.now().strftime(self.df),table.name))

            self.cursor.execute('BEGIN TRANSACTION;')
            self.pg_cur.execute("ALTER TABLE {}.\"{}\" DISABLE TRIGGER ALL;\n".format(schema.name, table.name))
            self.cursor.execute(self.select_query(schema, table))
            count = 0
            batch = self.cursor.fetchmany(50)
            while len(batch) > 0:
                count+=len(batch)
                self.log.info("[{}]:  Старт транзакции загрузки фрагмента размера {}"
                              .format(datetime.datetime.now().strftime(self.df),len(batch)))

                batch_query = 'BEGIN TRANSACTION;\n'
                for row in batch:
                    batch_query += self.insert_query(schema, table, row) + ";\n"
                self.pg_cur.execute(batch_query)
                batch_query += 'COMMIT TRANSACTION;\n'
                self.log.info("[{}]:  Финиш транзакции загрузки фрагмента"
                              .format(datetime.datetime.now().strftime(self.df)))
                batch = self.cursor.fetchmany(50)

            self.pg_cur.execute("ALTER TABLE {}.\"{}\" ENABLE TRIGGER ALL;\n".format(schema.name, table.name))
            self.cursor.execute('COMMIT;')
            self.log.info("[{}]:  Записей добавлено: {}"
                          .format(datetime.datetime.now().strftime(self.df),count))
        self.pg_cur.execute('COMMIT TRANSACTION;')
        end_time = datetime.datetime.now()
        diff = end_time - start_time
        mills = float(diff.microseconds/1000)
        sec = float(mills/1000)
        min = float(sec/60)
        hrs = float(min/60)
        self.log.info(" ")
        self.log.info('[{0}]: Время выполнения переноса данных: {1:.0f} ч {2:.0f} м {3:.0f} с {4:.0f} мс'.format(datetime.datetime.now().strftime(self.df),
                                                                   hrs,min,sec, mills))
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
        query = 'INSERT INTO {}."{}" ({}) VALUES ({})'\
            .format(schema.name, table.name,', '.join(fields),', '.join(_values))

        return query