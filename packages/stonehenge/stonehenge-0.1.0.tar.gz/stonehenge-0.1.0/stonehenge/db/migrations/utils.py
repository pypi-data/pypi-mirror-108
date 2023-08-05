import json
import re
import os
from typing import Dict, List

from stonehenge.application import Application
from stonehenge.db.databases import DBColumn
from stonehenge.db.fields import Field
from stonehenge.db.databases import Database
from stonehenge.db.migrations.exceptions import UnappliedMigrationException
from stonehenge.db.operations import (
    Operation,
    AddColumnOperation,
    CreateTableOperation,
    RemoveColumnOperation,
    UnknownOperationException,
)
from stonehenge.db.utils import get_database_for_model
from stonehenge.db.migrations.migration import Migration
from stonehenge.db.migrations.types import DatabaseMigrationState, MigrationState

index_pattern = re.compile("Migration_(?P<index>\\d+).json")


def check_for_unapplied_migrations(app: Application):
    for db in app.databases:
        migration_files = os.listdir(app.MIGRATIONS_DIR)
        for migration_file in migration_files:
            if index_match := index_pattern.match(migration_file):
                index = index_match.groupdict()["index"]
            else:
                continue
            query = "SELECT * FROM %s WHERE migration_index = %s"
            params = (app.MIGRATIONS_TABLE_NAME, index)
            results = db.run_query(query, params, return_operation="fetch_one")
            if not results:
                raise UnappliedMigrationException(migration_file)


def create_migrations_table(databases: List[Database], migrations_table_name: str):
    """Create a table to store applied migrations"""
    for database in databases:
        if database.read_only:
            # Unmanaged database
            continue
        if database.check_table_exists(migrations_table_name):
            # Table exists
            continue
        database.create_table(
            migrations_table_name,
            columns=[
                DBColumn(
                    field_name="migration_index",
                    null=False,
                    column_type="INTEGER",
                    primary_key=True,
                ),
            ],
        )


def make_migrations_directory(migrations_dir):
    """Create directory at app's migration location and __init__file within"""
    if not os.path.exists(migrations_dir):
        os.makedirs(migrations_dir)


def get_expected_migration_state(app: Application) -> MigrationState:
    state: MigrationState = {}
    for database in app.databases:
        state[database.label] = {}

    for model in app.models:
        model_data: Dict[str, DBColumn] = {}
        for field_name, field in model._db_fields.items():
            column = DBColumn(
                column_type=field.db_column_type,
                field_name=field_name,
                null=field.null,
                length=getattr(field, "max_length", None),
                primary_key=field.primary_key,
            )
            model_data[field_name] = column
        database = get_database_for_model(app, model)
        model_name = model._get_db_name()
        state[database.label][model_name] = model_data
    return state


def get_current_migration_state(app: Application) -> MigrationState:
    """Examine most recent migration file for app state and return as JSON"""
    state: MigrationState = {}
    for db in app.databases:
        state[db.label] = {}
        for table_name in db.list_tables(app.MIGRATIONS_TABLE_NAME):
            table_state = db.describe_table(table_name)
            state[db.label][table_name] = table_state

    return state


def get_unapplied_migration_operations(
    databases: List[Database],
    current_state: MigrationState,
    expected_state: MigrationState,
) -> List[Operation]:
    operations: List[Operation] = []
    for database in databases:
        current_db_state = current_state[database.label]
        expected_db_state = expected_state[database.label]
        db_operations = get_unapplied_migration_operations_for_db(
            current_db_state=current_db_state,
            expected_db_state=expected_db_state,
            db_label=database.label,
        )
        operations += db_operations

    return operations


def get_unapplied_migration_operations_for_db(
    current_db_state: DatabaseMigrationState,
    expected_db_state: DatabaseMigrationState,
    db_label: str,
) -> List[Operation]:
    operations: List[Operation] = []
    for model_name, model_data in expected_db_state.items():
        if model_name not in current_db_state:
            # Create model
            operation = CreateTableOperation(
                columns=list(model_data.values()),
                table_name=model_name,
                db_label=db_label,
            )
            operations.append(operation)
        elif current_db_state[model_name] != model_data:
            # Modify operation
            current_model_state = current_db_state[model_name]
            alter_operations = get_alter_table_operations_for_model(
                current_model_state=current_model_state,
                db_label=db_label,
                expected_model_state=model_data,
                table_name=model_name,
            )
            operations += alter_operations

    for model_name, model_data in current_db_state.items():
        if model_name not in expected_db_state:
            # Delete model
            raise Exception("DELETE NOT SUPPORTED YET")
    return operations


def get_migration_from_filepath(filepath: str, migrations_dir: str) -> Migration:
    with open(filepath, "r") as f:
        contents = json.loads(f.read())
    operations: List[Operation] = []
    for operation_json in contents["operations"]:
        if operation_json["operation_type"] == "CREATE_TABLE":
            operations.append(get_create_table_operation_from_json(operation_json))
        elif operation_json["operation_type"] == "ADD_COLUMN":
            operations.append(AddColumnOperation.from_json(operation_json))
        else:
            raise UnknownOperationException(operation_json["operation_type"])
    return Migration(operations=operations, migrations_dir=migrations_dir)


def get_alter_table_operations_for_model(
    current_model_state,
    db_label: str,
    expected_model_state,
    table_name: str,
) -> List[Operation]:
    operations: List[Operation] = []

    for field_name, column in expected_model_state.items():
        if field_name not in current_model_state:
            operations.append(
                AddColumnOperation(
                    column=column,
                    db_label=db_label,
                    table_name=table_name,
                )
            )
        elif column != current_model_state[field_name]:
            # TODO implement
            pass

    for field_name, column in current_model_state.items():
        if field_name not in expected_model_state:
            operations.append(
                RemoveColumnOperation(
                    db_label=db_label,
                    field_name=field_name,
                    table_name=table_name,
                )
            )
    return operations


def get_create_table_operation_from_json(operation_json) -> CreateTableOperation:
    columns = []
    for column_json in operation_json["columns"]:
        columns.append(DBColumn(**column_json))

    return CreateTableOperation(
        columns=columns,
        table_name=operation_json["table_name"],
        db_label=operation_json["db_label"],
    )
