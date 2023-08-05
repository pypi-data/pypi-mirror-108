import os
from stonehenge.db.operations import InsertOperation

from stonehenge.application import Application
from stonehenge.db.migrations.migration import Migration
from stonehenge.db.migrations.utils import (
    check_for_unapplied_migrations,
    create_migrations_table,
    get_current_migration_state,
    get_expected_migration_state,
    get_migration_from_filepath,
    get_unapplied_migration_operations,
    make_migrations_directory,
)


def makemigrations(app: Application):
    make_migrations_directory(app.MIGRATIONS_DIR)
    create_migrations_table(app.databases, app.MIGRATIONS_TABLE_NAME)
    check_for_unapplied_migrations(app)

    expected_state = get_expected_migration_state(app)
    current_state = get_current_migration_state(app)
    required_operations = get_unapplied_migration_operations(
        current_state=current_state,
        databases=app.databases,
        expected_state=expected_state,
    )
    if required_operations:
        migration = Migration(
            operations=required_operations,
            migrations_dir=app.MIGRATIONS_DIR,
        )
        filepath = migration.save_to_file()
        print(f"{filepath} created")


def migrate(app: Application):
    """Read migrations directory for unapplied migrations and perform them"""
    if not os.path.isdir(app.MIGRATIONS_DIR):
        print("No migrations found. Not applying.")
        return
    for migration_filename in os.listdir(app.MIGRATIONS_DIR):
        filepath = os.path.join(app.MIGRATIONS_DIR, migration_filename)
        migration = get_migration_from_filepath(
            filepath=filepath, migrations_dir=app.MIGRATIONS_DIR
        )
        for db in app.databases:
            db_label = migration.operations[0].db_label
            if db_label != db.label:
                continue

            # Check whether migration has been applied
            migration_index = migration_filename[10]
            query = "SELECT * FROM %s WHERE migration_index = %s"
            params = (app.MIGRATIONS_TABLE_NAME, migration_index)
            results = db.run_query(query, params, return_operation="fetch_one")
            if results:
                continue

            # Apply migration
            for operation in migration.operations:
                db.apply_operation(operation)

            # Mark migration as applied
            insert_operation = InsertOperation(
                db_label=db.label,
                table_name=app.MIGRATIONS_TABLE_NAME,
                values={"migration_index": migration_index},
            )
            db.apply_operation(insert_operation)
            print(f"Migration_{migration_index}.json applied")
