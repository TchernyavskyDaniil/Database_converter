import pyodbc

from common.ram import Schema, Domain, Table, Field, Constraint, Index, ConstraintDetail, IndexDetail


class MssqlToRam:
    def __init__(self,url):
        self.url = url
        self.conn = pyodbc.connect(url)
        self.cursor = self.conn.cursor()

    def get_schemas(self):
        query = """
        SELECT s.schema_id AS id
              ,s.name AS name
              ,NULL AS fulltext_engine
              ,NULL AS version
              ,NULL AS description
              FROM sys.schemas AS s
              ORDER BY s.schema_id
        """
        self.cursor.execute(query)
        schemas_data = self._get_result()
        schemas = {}
        for row in schemas_data:
            schema,id  = self.construct_schema(row)
            schemas[id] = schema
        return schemas

    def construct_schema(self,row):
        schema = Schema()
        id = None
        for a in row:
            if a == 'name':
                schema.name = row[a]
            elif a == 'fulltext_engine':
                schema.fulltext_engine = row[a]
            elif a == 'version':
                schema.version = row[a]
            elif a == 'description':
                schema.descr = row[a]
            elif a == 'id':
                id = row[a]
            else:
                raise Exception("Error parse schema attribute {}".format(a))
        return schema, id

    def get_domains(self):
        query = """
        SELECT ROW_NUMBER() OVER ( ORDER BY col.object_id ,col.column_id)                    AS id
        ,col.name + CAST(col.object_id AS VARCHAR(20)) AS name
        ,NULL AS description
        ,type.name AS data_type_name
        ,col.max_length AS length
        ,col.max_length AS char_length
        ,col.precision AS precision
        ,col.scale AS scale
        ,NULL AS width,NULL AS align,NULL AS show_null,NULL AS show_lead_nulls
        ,NULL AS thousands_separator,NULL AS summable,NULL AS case_sensitive
        FROM sys.columns AS col
        INNER JOIN sys.types AS type
            ON col.system_type_id = type.system_type_id
            AND col.user_type_id = type.user_type_id
        """

        self.cursor.execute(query)
        domains = []
        domains_data = self._get_result()
        for row in domains_data:
            domain,id = self.construct_domain(row)
            domains.append(domain)

        return domains

    def construct_domain(self,row):
        domain = Domain()
        id = ""
        for a in row:
            if a == 'name':
                domain.name = row[a]
            elif a == 'data_type_name':
                domain.type = row[a]
            elif a == 'align':
                domain.align = row[a]
            elif a == 'width':
                domain.width = row[a]
            elif a == 'char_length':
                domain.char_length = row[a]
            elif a == 'description':
                domain.descr = row[a]
            elif a == 'length':
                domain.length = row[a]
            elif a == 'scale':
                domain.scale = row[a]
            elif a == 'precision':
                domain.precision = row[a]
            elif a == 'case_sensitive':
                domain.case_sensitive = row[a]
            elif a == 'show_null':
                domain.show_null = row[a]
            elif a == 'show_lead_nulls':
                domain.show_lead_nulls = row[a]
            elif a == 'thousands_separator':
                domain.thousands_separator = row[a]
            elif a == 'summable':
                domain.summable = row[a]
            elif a == 'id':
                id = row[a]
            else:
                raise Exception("Error parse domain attribute {}".format(a))
        return domain,id

    def get_tables(self,schemas):
        query = """
        SELECT
         tab.object_id AS id
        ,tab.schema_id AS schema_id
        ,tab.name AS name
        ,NULL AS description
        ,NULL AS can_add
        ,NULL AS can_edit
        ,NULL AS can_delete
        ,NULL AS temporal_mode
        ,NULL AS means
        FROM sys.tables AS tab
        """
        self.cursor.execute(query)
        tables_data = self._get_result()
        tables = {}
        for row in tables_data:
            table,table_id,schema_id = self.construct_table(row)
            tables[table_id] = table
            schemas[schema_id].tables.append(table)
        return tables, schemas

    def construct_table(self, row):
        table_id = None
        schema_id = None
        table = Table()
        for a in row:
            if a == 'name':
                table.name = row[a]
            elif a == 'description':
                table.descr = row[a]
            elif a == 'temporal_mode':
                table.ht_table_flags = row[a]
            elif a == 'access_level':
                table.access_level = row[a]
            elif a == 'can_add':
                table.add = row[a]
            elif a == 'can_edit':
                table.edit = row[a]
            elif a == 'can_delete':
                table.delete = row[a]
            elif a == 'means':
                table.means = row[a]
            elif a == 'schema_id':
                schema_id = row[a]
            elif a == 'id':
                table_id = row[a]
            else:
                raise Exception("Error parse table attribute {}".format(a))
        return table,table_id,schema_id

    def get_fields(self,tables):
        query = """
        SELECT ROW_NUMBER() OVER ( ORDER BY field.object_id ,field.column_id)                         AS id
        ,field.object_id AS table_id
        ,field.name AS name
        ,field.collation_name AS russian_short_name
        ,field.name + CAST(field.object_id AS VARCHAR(20)) AS domain_name
        ,NULL AS description,NULL AS can_input,NULL AS can_edit,NULL AS required
        ,NULL AS show_in_grid,NULL AS show_in_details,NULL AS is_mean
        ,field.is_computed AS autocalculated
        FROM sys.columns AS field
        ORDER BY field.column_id

        """
        self.cursor.execute(query)
        fields = {}
        fields_data = self._get_result()
        for row in fields_data:
            field,field_id,table_id = self.construct_field(row)
            fields[field_id] = field
            if table_id not in tables:
                continue
            tables[table_id].fields.append(field)
        return fields, tables

    def construct_field(self,row):
        field = Field()

        field_id = None
        table_id = None

        for a in row:

            if a == 'name':
                field.name = row[a]
            elif a == 'russian_short_name':
                field.rname = row[a]
            elif a == 'domain_name':
                field.domain = row[a]
            elif a == 'type':
                field.type = row[a]
            elif a == 'description':
                field.description = row[a]
            elif a == 'can_input':
                field.can_input = row[a]
            elif a == 'can_edit':
                field.can_edit = row[a]
            elif a == 'show_in_grid':
                field.show_in_grid = row[a]
            elif a == 'show_in_details':
                field.show_in_details = row[a]
            elif a == 'is_mean':
                field.is_mean = row[a]
            elif a == 'autocalculated':
                field.autocalculated = row[a]
            elif a == 'required':
                field.required = row[a]
            elif a == 'id':
                field_id = row[a]
            elif a == 'table_id':
                table_id = row[a]
            else:
                raise Exception("Error parse field attribute {}".format(a))
        return field, field_id, table_id

    def get_constraints(self,tables):
        query = """
         SELECT con.object_id AS id
                ,con.parent_object_id AS table_id
                ,con.name AS name
                ,'PRIMARY' AS constraint_type
                ,NULL AS reference,NULL AS has_value_edit
                ,NULL AS cascading_delete,NULL AS expression
            FROM sys.objects          AS con
            WHERE con.type = 'PK'
            UNION ALL
            SELECT con.object_id AS id
                ,con.parent_object_id AS table_id
                ,con.name AS name
                ,'FOREIGN' AS constraint_type
                ,OBJECT_NAME(con.referenced_object_id) AS reference
                ,NULL AS has_value_edit
                ,NULL AS cascading_delete,NULL AS expression
            FROM sys.foreign_keys AS con
            """
        self.cursor.execute(query)
        constraints = {}
        constraints_data = self._get_result()
        for row in constraints_data:
            constraint,constraint_id,table_id = self.construct_constraint(row)
            constraints[constraint_id] = constraint
            if table_id not in tables:
                continue
            tables[table_id].constraints.append(constraint)
            if constraint.reference in tables.keys():
                constraint.reference = tables[constraint.reference].name
        return constraints, tables

    def construct_constraint(self,row):
        constraint = Constraint()

        if row is None:
            return constraint

        constraint_id = None
        table_id = None

        for a in row:
            if a == 'name':
                constraint.name = row[a]
            elif a == 'constraint_type':
                constraint.kind = row[a]
            elif a == 'items':
                constraint.items = row[a]
            elif a == 'reference':
                constraint.reference = row[a]
            elif a == 'expression':
                constraint.expression = row[a]
            elif a == 'has_value_edit':
                constraint.has_value_edit = True
            elif a == 'full_cascading_delete':
                constraint.full_cascading_delete = True
            elif a == 'cascading_delete':
                constraint.cascading_delete = True
            elif a == 'id':
                constraint_id = row[a]
            elif a == 'table_id':
                table_id = row[a]
            else:
                raise Exception("Error parse constraint attribute {}".format(a))
        return constraint,constraint_id,table_id

    def get_indexes(self,tables):
        query = """
        SELECT ROW_NUMBER() OVER ( ORDER BY ind.object_id,ind.index_id )                         AS id
        ,ind.object_id AS table_id
        ,ind.name AS name
        ,CASE WHEN ind.is_unique = 1
				THEN 'uniqueness'
			    ELSE NULL
         END AS kind
        FROM sys.indexes AS ind
        """
        self.cursor.execute(query)
        indexes = {}
        indexes_data = self._get_result()
        for row in indexes_data:
            index, index_id, table_id = self.construct_index(row)
            if table_id in tables:
                tables[table_id].indexes.append(index)
            indexes[index_id] = index

        return tables, indexes

    def construct_index(self,row):
        index = Index()

        if row is None:
            return index

        index_id = None
        table_id = None

        for a in row:
            if a == 'name':
                index.name = row[a]
            elif a == 'field':
                index.field = row[a]
            elif a == 'kind':
                index.kind = row[a]
            elif a == 'uniqueness':
                index.uniqueness = True
            elif a == 'fulltext':
                index.fulltext = True
            elif a == 'id':
                index_id = row[a]
            elif a == 'table_id':
                table_id = row[a]
            elif a == 'descend':
                index.descend = row[a]
            else:
                raise Exception("Error parse index attribute {}".format(a))
        return index, index_id, table_id

    def get_constraint_details(self, constraints):
        query = """SELECT ROW_NUMBER() OVER ( ORDER BY det.constraint_id ,det.field_name) AS id
        ,det.constraint_id AS constraint_id
        ,det.field_name AS field_name
        FROM (
		SELECT
			 con.object_id AS constraint_id
			,det.COLUMN_NAME AS field_name
		FROM sys.objects AS con
		INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS det
			ON con.name = det.CONSTRAINT_NAME
		WHERE con.type = 'PK'
		UNION ALL
		SELECT
			 con.object_id AS constraint_id
			,COL_NAME(det.parent_object_id, det.parent_column_id) AS field_name
		FROM sys.foreign_keys AS con
		INNER JOIN sys.foreign_key_columns AS det
			ON con.object_id = det.constraint_object_id
        ) AS det
        """
        self.cursor.execute(query)
        constraint_details = {}
        details_data = self._get_result()
        for row in details_data:
            detail, detail_id, constraint_id = self.construct_constr_det(row)
            constraints[constraint_id].details.append(detail)
            constraint_details[detail_id] = detail
        return constraints, constraint_details

    def construct_constr_det(self, row):
        detail = ConstraintDetail()

        detail_id = None
        constraint_id = None

        for attr in row:
            if attr == 'field_name':
                detail.value = row[attr]
            elif attr == 'id':
                detail_id = row[attr]
            elif attr == 'constraint_id':
                constraint_id = row[attr]
            else:
                raise Exception("Error parse attribute {}".format(attr), self)
        return detail, detail_id, constraint_id

    def get_index_details(self,indexes):
        query = """
        SELECT ROW_NUMBER() OVER( ORDER BY detail.object_id,detail.index_id) AS id
        ,ind.id AS index_id
        ,col.name AS field_name
        ,NULL AS expression
        ,detail.is_descending_key AS descend
        FROM
        (
            SELECT
                ROW_NUMBER() OVER( ORDER BY ind.object_id,ind.index_id) AS id
                ,ind.object_id AS table_id
                ,ind.index_id AS index_id
                ,ind.name
            FROM sys.indexes   AS ind
        ) AS ind
        JOIN sys.index_columns AS detail
            ON detail.object_id = ind.table_id
            AND detail.index_id = ind.index_id
        INNER JOIN sys.columns AS col
            ON detail.column_id = col.column_id
            AND detail.object_id = col.object_id
        ORDER BY detail.column_id
        """

        self.cursor.execute(query)
        index_details = {}
        details_data = self._get_result()
        for row in details_data:
            detail, detail_id,index_id = self.construct_index_det(row)
            index_details[detail_id] = detail
            indexes[index_id].details.append(detail)
        return index_details, indexes

    def construct_index_det(self,attr_dict):
        detail = IndexDetail()
        detail_id = None
        index_id = None

        for attr in attr_dict:
            if attr == 'field_name':
                detail.value = attr_dict[attr]
            elif attr == 'expression':
                detail.expression = attr_dict[attr]
            elif attr == 'descend':
                detail.descend = attr_dict[attr]
            elif attr == 'id':
                detail_id = attr_dict[attr]
            elif attr == 'index_id':
                index_id = attr_dict[attr]
            else:
                raise Exception("Error parse attribute {}".format(attr), self)
        return detail, detail_id, index_id

    def load_data(self):
        schemas = self.get_schemas()

        domains = self.get_domains(schemas)

        tables,schemas = self.get_tables(schemas)
        for schema in schemas.values():
            if len(schema.tables) > 0:
                schema.domains = domains

        fields,tables = self.get_fields(tables)
        constraints,tables = self.get_constraints(tables)
        tables,indexes = self.get_indexes(tables)

        self.get_constraint_details(constraints)
        self.get_index_details(indexes)
        return schemas

    def _get_result(self):
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


