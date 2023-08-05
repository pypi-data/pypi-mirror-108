from typing import Dict
from stonehenge.db.columns import DBColumn


TableMigrationState = Dict[str, DBColumn]
DatabaseMigrationState = Dict[str, TableMigrationState]
MigrationState = Dict[str, DatabaseMigrationState]
