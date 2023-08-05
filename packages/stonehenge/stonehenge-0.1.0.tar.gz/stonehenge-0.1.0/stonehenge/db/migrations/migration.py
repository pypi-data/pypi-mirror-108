import json
import os

from typing import List
from stonehenge.db.operations import Operation
from stonehenge.db.migrations.exceptions import UnappliedMigrationException


class Migration:
    def __init__(
        self,
        operations: List[Operation],
        migrations_dir: str,
    ):
        self.operations = operations
        self.migrations_dir = migrations_dir

    def save_to_file(self) -> str:
        next_migration_index = self.get_next_migration_index()
        filename = f"Migration_{next_migration_index}.json"
        filepath = os.path.join(self.migrations_dir, filename)

        if os.path.isfile(filepath):
            raise UnappliedMigrationException(filename)

        with open(filepath, "w+") as f:
            content = self.to_json()
            content_str = json.dumps(content, indent=4)
            f.write(content_str)
        return filename

    def get_next_migration_index(self) -> int:
        highest = 1
        for filename in os.listdir(self.migrations_dir):
            try:
                index = int(filename[10])
            except ValueError:
                continue
            if index >= highest:
                highest = index + 1
        return highest

    def to_json(self):
        return {
            "operations": [o.to_json() for o in self.operations],
        }
