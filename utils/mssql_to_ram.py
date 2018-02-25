import pyodbc

from common.ram import Schema, Index, Constraint, Field, Domain, Table
from utils.ram_to_pg_ddl import RamToPgDdl


class MssqlToRam:
    def __init__(self,url):
        self.url = url
        self.conn = pyodbc.connect(url)
        self.cursor = self.conn.cursor()

    def _get_result(self):
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def load(self,schema_name):
        schema = Schema()
        schema.name = schema_name
        schema.tables = self.load_table(schema)
        return schema

    def load_table(self, schema: Schema):
        self.cursor.execute("""select 
            t.name, 
            OBJECTPROPERTY(t.object_id, 'HasInsertTrigger') as addition, 
            OBJECTPROPERTY(t.object_id, 'HasUpdateTrigger') as edition, 
            t.temporal_type
        from sys.tables as t
        join sys.schemas as s
        on t.schema_id = s.schema_id
        where s.name = ?""", schema.name)
        rows = self._get_result()
        list = []
        for row in rows:
            table = Table()
            # print(table)
            table.name = row['name']
            table.add = bool(row['addition'])
            table.edit = bool(row['edition'])
            table.temporal_mode = bool(row['temporal_type'])
            table.indexes = self.load_indices(schema.name, table.name)
            table.constraints = self.load_constraints(schema.name, table.name)
            table.fields = self.load_fields(table.name)

            list.append(table)
        return list

    def load_indices(self, schema_name: str, table_name: str):
        self.cursor.execute(""" select 
            ind.name as index_name, 
            ind.is_unique, 
            fti.object_id as is_fulltext, 
            c.name as field_name
        from sys.indexes as ind
        left join sys.fulltext_indexes as fti
        on ind.object_id = fti.object_id
        join sys.index_columns as ic
        on ind.object_id = ic.object_id and ind.index_id = ic.index_id
        join sys.columns as c
        on ind.object_id = c.object_id and ic.column_id = c.column_id
        where ind.object_id = OBJECT_ID(?);
          """, "{0}.{1}".format(schema_name, table_name))
        rows = self._get_result()
        list = []
        for row in rows:
            index = Index()
            # print(row)
            index.name = row['index_name']
            if bool(row['is_unique']):
                index.uniqueness = True
            elif bool(row['is_fulltext']):
                index.fulltext = True

            index.field = row['field_name']
            list.append(index)
        return list

    def load_constraints(self, schema_name: str, table_name: str):
        self.cursor.execute("""select 
            kc.name, 
            KCU.COLUMN_NAME as items, 
            kc.unique_index_id as unique_key_index
        from sys.tables as t
        join sys.key_constraints as kc
        on t.object_id = kc.parent_object_id
        join INFORMATION_SCHEMA.KEY_COLUMN_USAGE as KCU
        on KCU.CONSTRAINT_NAME = kc.name
        where t.object_id = object_id(?);""", "{0}.{1}".format(schema_name, table_name))
        rows = self._get_result()
        primary = []
        for row in rows:
            # print(row)
            constraint = Constraint()
            constraint.name = row['name']
            constraint.items = row['items']
            constraint.kind = "PRIMARY"
            constraint.unique_key_id = row['unique_key_index']
            primary.append(constraint)

        self.cursor.execute("""select 
            fk.name as name, 
            ac.name as items, 
            tt.name as reference, 
            fk.delete_referential_action as cascading_delete
        from sys.tables as t
        join sys.all_columns as ac
        on t.object_id = ac.object_id
        join sys.foreign_key_columns as fkc
        on ac.column_id = fkc.parent_column_id and t.object_id = fkc.parent_object_id
        join sys.foreign_keys as fk
        on fkc.constraint_object_id = fk.object_id
        join sys.tables as tt
        on tt.object_id = fk.referenced_object_id
        where t.object_id = object_id(?);""", "{0}.{1}".format(schema_name, table_name))
        rows = self._get_result()
        foreign = []
        for row in rows:
            # print(row)
            constraint = Constraint()
            constraint.name = row['name']
            constraint.kind = "FOREIGN"
            constraint.items = row['items']
            constraint.reference = row['reference']
            constraint.cascading_delete = bool(row['cascading_delete'])
            foreign.append(constraint)

        return primary + foreign

    def load_fields(self, table_name: str):
        self.cursor.execute("""select 
            COLUMN_NAME as name, 
            t.name as dom,
            ORDINAL_POSITION as position, 
            sc.is_identity as edit,
            sc.is_hidden as show_in_grid,
            sc.is_computed as autocalculated,
            sc.is_nullable as required,
            col.DATA_TYPE,
            sc.scale,
            sc.precision,
            sc.max_length
        from INFORMATION_SCHEMA.TABLES as tbl
        left join INFORMATION_SCHEMA.COLUMNS as col
        on col.TABLE_NAME = tbl.TABLE_NAME
        left join sys.columns as sc
        on sc.object_id = object_id(tbl.table_schema + '.' + tbl.table_name) and sc.NAME = col.COLUMN_NAME
        left join sys.types as t
        on col.DATA_TYPE = t.name
        where tbl.TABLE_NAME = ?;""", table_name)
        rows = self._get_result()
        list = []
        for row in rows:
            # print(row)
            field = Field()
            field.name = row['name']
            field.domain = row['dom']
            field.position = str(row['position'])
            field.edit = row['edit']
            field.show_in_grid = row['show_in_grid']
            field.autocalculated = row['autocalculated']
            field.required = row['required']
            field.input = not (field.autocalculated or field.edit)
            domain = Domain()
            domain.char_length = str(row['max_length'])
            domain.precision = str(row['precision'])
            domain.scale = str(row['scale'])
            domain.type = row['DATA_TYPE']
            domain.type = RamToPgDdl.ram_types_to_pg(domain.type)
            field.domain = domain
            list.append(field)
        return list
