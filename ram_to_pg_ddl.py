
class RamToPgDdl:
    def __init__(self, ram_model):

        self.schema = ram_model

        self.constraint_id = 0
        self.index_id = 0

        self.ddl = ""

    def generate(self):
        self.__generate_schema()
        self.__generate_domains()
        self.__generate_tables()
        self.__generate_constraints()
        self.__generate_indexes()

        return self.ddl

    def write_to_file(self,filename):

        with open(filename, "w", encoding='utf-8') as f:
            f.write(self.ddl)

    def write(self, query):
        self.ddl+=query
        self.ddl+="\n"

    @staticmethod
    def ram_types_to_pg(data_type):
        data_type = data_type.upper()
        if data_type in ['STRING', 'MEMO','FIXEDCHAR', 'SYSNAME', 'NVARCHAR', 'VARCHAR']:
            return 'VARCHAR'
        elif data_type in ['UNIQUEIDENTIFIER', 'MONEY', 'SQL_VARIANT', 'BIT']:
            return 'varchar(200)'

        elif data_type == 'SMALLINT':
            return 'SMALLINT'
        elif data_type in ['INTEGER' , 'INT']:
            return 'INTEGER'
        elif data_type == 'BIGINT':
            return 'BIGINT'
        elif data_type in ['WORD','TINYINT']:
            return 'SMALLINT'
        elif data_type == 'BOOLEAN':
            return 'BOOLEAN'
        elif data_type == 'FLOAT':
            return 'FLOAT'
        elif data_type  in ['FLOAT', 'REAL']:
            return 'REAL'
        elif data_type == 'CURRENCY':
            return 'NUMERIC'
        elif data_type == 'BCD':
            return 'DECIMAL'
        elif data_type == 'DATE':
            return 'DATE'
        elif data_type == 'TIME':
            return 'TIME'
        elif data_type == 'DATETIME':
            return 'TIMESTAMP'
        elif data_type == 'TIMESTAMP':
            return 'TIMESTAMP'
        elif data_type == 'BYTES':
            return 'BYTEA'
        elif data_type == 'VARBYTES':
            return 'BYTEA'
        elif data_type in ['BLOB' ,'GRAPHIC']:
            return 'BYTEA'
        elif data_type in ['FMTMEMO','NTEXT', 'NCHAR', 'CHAR', 'BLOB', 'VARBINARY', 'BINARY', 'IMAGE']:
            return 'TEXT'
        elif data_type == 'FIXEDCHAR':
            return 'VARCHAR'
        elif data_type == 'WIDESTRING':
            return 'TEXT'
        elif data_type == 'LARGEINT':
            return 'BIGINT'
        elif data_type == 'COMP':
            return 'BIGINT'
        elif data_type == 'ARRAY':
            return 'ARRAY'
        elif data_type == 'FIXEDWIDECHAR':
            return 'TEXT'
        elif data_type == 'WIDEMEMO':
            return 'TEXT'
        elif data_type == 'CODE':
            return 'TEXT'
        elif data_type == 'RECORDID':
            return 'INTEGER'
        elif data_type == 'SET':
            return 'ARRAY'
        elif data_type == 'PERIOD':
            return 'INTERVAL'
        elif data_type == 'BYTE':
            return 'BYTEA'
        elif data_type in ['DATETIME','DATETIMEOFFSET']:
            return 'timestamp'
        else:
            print(data_type)

    def __generate_schema(self):
        ddl = "CREATE SCHEMA {};".format(self.schema.name)
        self.write(ddl)

    def __generate_domains(self):
        for domain in self.schema.domains:

            ddl = "CREATE DOMAIN {0}.\"{1}\" AS {2} {3};"

            schema_name = self.schema.name

            name = domain.name
            type = self.ram_types_to_pg(domain.type)
            if type == 'VARCHAR' and str(is_not_empty(domain.char_length)) and domain.char_length!=-1:
                length = "({0})".format(str(domain.char_length))
            else:
                length = ""
            self.write(ddl.format(schema_name, name, type, length))
        self.write('\n')

    def __generate_tables(self):
        for table in self.schema.tables:

            ddl = "CREATE TABLE {}.\"{}\" ({});"

            fields = ",".join(
                [self.__generate_fields(
                    field.name, self.schema.name, field.domain)
                      for field in table.fields])
            ddl = ddl.format(self.schema.name,table.name, fields)
            self.write(ddl)
        self.write('\n')

    def __generate_fields(self,field_name,schema_name,domain):
        return """\"{}\" {}.\"{}\"""" \
            .format(field_name, schema_name, domain)

    def __generate_constraints(self):
        schema_name = self.schema.name
        foreign = ""
        primary = ""
        for table in self.schema.tables:
            for constraint in table.constraints:
                details = []
                for det in constraint.details:
                    detail = r'"' + det.value + r'"'
                    details.append(detail)

                if constraint.kind.lower() == 'primary':
                    str = """PRIMARY KEY ({})""" \
                        .format(', '.join(details))
                    primary += """ALTER TABLE {}."{}" ADD {};\n""" \
                        .format(schema_name, table.name, str)

                elif constraint.kind.lower() == 'foreign':
                    str = """FOREIGN KEY ({}) REFERENCES {}."{}" DEFERRABLE""" \
                        .format(', '.join(details), schema_name,
                                constraint.reference, constraint.name)
                    foreign+= """ALTER TABLE {}."{}" ADD {};\n""" \
                        .format(schema_name, table.name, str)

                else:
                    return ''
        self.write(primary + foreign)

    def __generate_indexes(self):
        schema_name = self.schema.name
        for table in self.schema.tables:
            for index in table.indexes:
                details = []
                for det in index.details:
                    detail = '\"' + det.value + '\"'
                    if det.expression:
                        detail += ' (' + det.expression + ')'
                    if not det.descend:
                        detail += ' ASC'
                    else:
                        detail += det.descend.upper()
                    details.append(detail)

                if len(details) == 0:
                    return ''

                ddl = """CREATE INDEX {} ON {}."{}"({});""" \
                    .format('"' + index.name + table.name + '"' if index.name else '',
                            schema_name, table.name, ', '.join(details))
                self.write(ddl)


def is_not_empty(value):
    return value is not None and value != ""
