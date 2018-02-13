class RamToPgDdl:
    def __init__(self, file, ram_model):

        self.schema = ram_model
        self.filename = file

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

    def write_to_file(self):

        with open(self.filename, "w", encoding='utf-8') as f:
            f.write(self.ddl)

    @staticmethod
    def ram_types_to_pg(data_type):
        if data_type == 'STRING':
            return 'VARCHAR'
        elif data_type == 'SMALLINT':
            return 'SMALLINT'
        elif data_type == 'INTEGER':
            return 'INTEGER'
        elif data_type == 'WORD':
            return 'SMALLINT'
        elif data_type == 'BOOLEAN':
            return 'BOOLEAN'
        elif data_type == 'FLOAT':
            return 'FLOAT'
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
        elif data_type == 'BLOB':
            return 'BYTEA'
        elif data_type == 'MEMO':
            return 'TEXT'
        elif data_type == 'GRAPHIC':
            return 'BYTEA'
        elif data_type == 'FMTMEMO':
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

    def __write(self, string, indent):
        self.ddl += indent + string + '\n'

    def __new_line(self):
        self.ddl += '\n\n'

    def __generate_schema(self):
        ddl = "CREATE SCHEMA {};".format(self.schema.name)
        self.ddl+=ddl

    def __generate_domains(self):
        for domain in self.schema.domains:

            ddl = "CREATE DOMAIN {0}.\"{1}\" AS {2} {3};"

            schema_name = self.schema.name;

            name = domain.name
            type = self.ram_types_to_pg(domain.type)

            if domain.char_length and str(is_not_empty(domain.char_length)):
                length = "({0})".format(str(domain.char_length))
            else:
                length = ""

            self.__write(ddl.format(schema_name, name, type, length), indent='')

            self.__new_line()

        self.ddl += '\n'

    def __generate_tables(self):
        for table in self.schema.tables:

            ddl = "CREATE TABLE {}.\"{}\" ({});\n"

            fields = ",".join(
                [self.__generate_fields(
                    field.name, self.schema.name, field.domain.name)
                      for field in table.fields])
            ddl = ddl.format(self.schema.name,table.name, fields)
            self.ddl+=ddl

    def __generate_fields(self,field_name,schema_name,domain):
        return """\"{}\" {}.\"{}\"""" \
            .format(field_name, schema_name, domain)

    def __generate_constraints(self):
        schema_name = self.schema.name
        for table in self.schema.tables:
            for constraint in table.constraints:

                if constraint.kind == 'PRIMARY':
                    self.ddl += ("ALTER TABLE {}.\"{}\"".format(schema_name,table.name));
                    self.ddl += "\t ADD "
                    items = constraint.items.replace(' ', '').replace(',', '","')
                    self.ddl += ("PRIMARY KEY (\"%s\");" % items)

                    self.ddl += '\n\n'

        for table in self.schema.tables:
            schema_name = self.schema.name
            for constraint in table.constraints:
                if constraint.kind == 'FOREIGN':
                    self.ddl += ("ALTER TABLE {}.\"{}\"".format(schema_name,table.name));
                    constraint_name = constraint.name if constraint.name is not None else self.__get_constraint_name()
                    self.ddl += "\t ADD CONSTRAINT {0} ".format(constraint_name)
                    self.ddl += (
                        "FOREIGN KEY (\"{}\") REFERENCES {}.\"{}\"{}" .format(
                            constraint.items, schema_name, constraint.reference,
                            " ON DELETE CASCADE;" if (
                                constraint.cascading_delete or constraint.full_cascading_delete) else ";"
                        )
                    )
                    self.ddl += '\n\n'

    def __generate_indexes(self):
        schema_name = self.schema.name
        for table in self.schema.tables:
            for index in table.indexes:
                items = index.field.replace(' ', '').replace(',', '","')

                ddl =  ("CREATE {} INDEX \"{}_{}_idx\" ON {}.\"{}\"(\"{}\");\n\n"
                             .format(
                                 "UNIQUE " if index.uniqueness else "",

                                 table.name,
                                 items.replace(' ', '').replace('"', '').replace(',', '_'),
                                schema_name,
                                 table.name,
                                 items

                             )
                    )
                self.ddl += ddl
    def __get_constraint_name(self):
        self.constraint_id += 1
        return 'constraint_' + str(self.constraint_id)

    def __get_index_name(self):
        self.index_id += 1
        return 'index_' + str(self.index_id)


def is_not_empty(value):
    return value is not None and value != ""
