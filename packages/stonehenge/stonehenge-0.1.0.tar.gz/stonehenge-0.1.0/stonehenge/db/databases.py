import sqlite3
from typing import Dict, List, Literal, Tuple, Union

from stonehenge.db.operations import (
    AddColumnOperation,
    CreateTableOperation,
    InsertOperation,
)
from stonehenge.db.migrations.types import TableMigrationState
from .columns import DBColumn


ReturnOperation = Union[
    None, Literal["fetch_all"], Literal["fetch_many"], Literal["fetch_one"]
]


class BaseDatabase:
    read_only = False

    def __init__(self, label: str, read_only: bool = False):
        self.label = label
        self.read_only = read_only

    def apply_operation(self, operation):
        if isinstance(operation, CreateTableOperation):
            self.create_table(
                table_name=operation.table_name, columns=operation.columns
            )
        elif isinstance(operation, InsertOperation):
            self.insert_row(
                table_name=operation.table_name,
                values=operation.values,
            )
        elif isinstance(operation, AddColumnOperation):
            self.add_column(
                table_name=operation.table_name,
                column=operation.column,
            )
        else:
            raise NotImplementedError(operation.__class__.__name__)

    def add_column(self, table_name: str, column: DBColumn):
        self.column = column
        self.table_name = table_name
        raise NotImplementedError

    def check_table_exists(self, table_name) -> bool:
        self.table_name = table_name
        raise NotImplementedError

    def create_table(self, table_name, columns: List[DBColumn]):
        self.table_name = table_name
        self.columns = columns
        raise NotImplementedError

    def insert_row(self, table_name: str, values: Dict):
        self.table_name = table_name
        self.values = values
        raise NotImplementedError

    def list_tables(self, migrations_table_name):
        self.migrations_table_name = migrations_table_name
        raise NotImplementedError

    def print_schema(self):
        pass


class SQLite3Database(BaseDatabase):
    def __init__(self, label: str, filename: str, read_only=False):
        self.filename = filename
        super().__init__(label=label, read_only=read_only)

    def get_connection(self):
        return sqlite3.connect(self.filename)

    def run_query(
        self,
        query_str: str,
        params: Tuple[Union[str, int], ...],
        return_operation: ReturnOperation = None,
    ):
        conn = self.get_connection()
        try:
            with conn:
                cur = conn.cursor()
                cur.execute(query_str % params)
                if not return_operation:
                    pass
                elif return_operation == "fetch_all":
                    return cur.fetchall()
                elif return_operation == "fetch_many":
                    return cur.fetchmany()
                elif return_operation == "fetch_one":
                    return cur.fetchone()
                else:
                    raise Exception(f"Unknown fetch operation {return_operation}")
        finally:
            conn.close()

    def add_column(self, table_name: str, column: DBColumn):
        query = "ALTER TABLE %s ADD %s %s"
        params = (table_name, column.field_name, column.get_sql_descriptor())
        self.run_query(query, params)

    def check_table_exists(self, table_name) -> bool:
        query_str = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s'"
        params = (table_name,)
        result = self.run_query(query_str, params, return_operation="fetch_one")
        return bool(result)

    def create_table(self, table_name, columns: List[DBColumn]):
        column_details = ", ".join([c.get_sql_descriptor() for c in columns])
        query_str = "CREATE TABLE %s (%s)"
        params = (table_name, column_details)
        self.run_query(query_str, params, return_operation="fetch_one")

    def describe_table(self, table_name: str) -> TableMigrationState:
        query = "pragma table_info('%s');"
        params = (table_name,)
        columns = self.run_query(query, params, return_operation="fetch_all")
        return {c[1]: DBColumn.from_sqlite3_pragma(c) for c in columns}

    def insert_row(self, table_name: str, values: Dict):
        query = "INSERT INTO %s (%s) VALUES (%s)"
        params = (table_name, ",".join(values.keys()), ",".join(values.values()))
        self.run_query(query, params, return_operation="fetch_one")

    def list_tables(self, migrations_table_name: str):
        query = "SELECT name FROM SQLITE_MASTER WHERE TYPE='table' ORDER BY name"
        results = self.run_query(query, (), "fetch_all")
        return filter(lambda t: t != migrations_table_name, [r[0] for r in results])

    def print_schema(self):
        connection = self.get_connection()

        for (tableName,) in connection.execute(
            """
                select NAME from SQLITE_MASTER where TYPE='table' order by NAME;
                """
        ):
            print("{}:".format(tableName))
            for (
                columnID,
                columnName,
                columnType,
                columnNotNull,
                columnDefault,
                columnPK,
            ) in connection.execute("pragma table_info('{}');".format(tableName)):
                print(
                    "  {id}: {name}({type}){null}{default}{pk}".format(
                        id=columnID,
                        name=columnName,
                        type=columnType,
                        null=" not null" if columnNotNull else "",
                        default=" [{}]".format(columnDefault) if columnDefault else "",
                        pk=" *{}".format(columnPK) if columnPK else "",
                    )
                )


class PostgreSQLDatabase(BaseDatabase):
    pass


class MySQLDatabase(BaseDatabase):
    pass


Database = Union[SQLite3Database]  # TODO: PGSQL and MySQL
