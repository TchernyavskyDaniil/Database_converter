import postgresql
import pyodbc

class DataTransfering:
    def __init__(self, db_name, pg_url, mssql_url):
        self.db_name = db_name
        self.pg_server = pg_url
        self.mssql_server = mssql_url
        self.mssql_con = pyodbc.connect(self.mssql_server)
        self.pg_con = postgresql.open(self.pg_server)
        self.cursor = self.mssql_con.cursor()


    def start(self,schema):
        self.pg_con.execute('BEGIN TRANSACTION;')
        self.pg_con.execute('SET CONSTRAINTS ALL DEFERRED;')
        for table in schema.tables:
            self.cursor.execute('BEGIN TRANSACTION;')
            self.cursor.execute(self.select_query(schema, table))
            rows = self.cursor.fetchall()
            query = ''
            for row in rows:
                s = "ALTER TABLE {}.\"{}\" DISABLE TRIGGER ALL;\n".format(schema.name, table.name)
                s += self.insert_query(schema, table, row) + ";\n"
                s += "ALTER TABLE {}.\"{}\" ENABLE TRIGGER ALL;\n".format(schema.name, table.name)
                # print(s)
                query += s

                self.pg_con.execute(s)
            self.cursor.execute('COMMIT;')

        self.pg_con.execute('COMMIT TRANSACTION;')

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