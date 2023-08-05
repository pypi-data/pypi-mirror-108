from __future__ import annotations
from typing import Any, Dict, List, Literal, Union
from stonehenge.db.columns import DBColumn

OperationAction = Union[
    Literal["ADD_COLUMN"],
    Literal["ALTER_TABLE"],
    Literal["CREATE_TABLE"],
    Literal["DROP_TABLE"],
]


class Operation:
    """Single action that needs to be performed on a database"""

    def __init__(self, db_label):
        self.db_label = db_label

    def __repr__(self):
        return f"DB Operation: {self.__class__.__name__}"

    def to_json(self):
        raise NotImplementedError


class CreateTableOperation(Operation):
    def __init__(self, columns: List[DBColumn], table_name: str, db_label: str):
        self.columns = columns
        self.table_name = table_name
        super().__init__(db_label=db_label)

    def __repr__(self):
        return f"Create Table Operation: {self.table_name}"

    def __dict__(self):
        return {
            "table_name": self.table_name,
        }

    def to_json(self):
        return {
            "db_label": self.db_label,
            "columns": [c.to_json() for c in self.columns],
            "operation_type": "CREATE_TABLE",
            "table_name": self.table_name,
        }


class AddColumnOperation(Operation):
    def __init__(self, db_label: str, table_name: str, column: DBColumn):
        self.column = column
        self.table_name = table_name

        super().__init__(db_label=db_label)

    @classmethod
    def from_json(cls, data) -> AddColumnOperation:
        column = DBColumn.from_json(data=data["column"])
        return AddColumnOperation(
            column=column,
            table_name=data["table_name"],
            db_label=data["db_label"],
        )

    def to_json(self):
        return {
            "column": self.column.to_json(),
            "db_label": self.db_label,
            "operation_type": "ADD_COLUMN",
            "table_name": self.table_name,
        }


class InsertOperation(Operation):
    def __init__(self, db_label: str, table_name: str, values: Dict[str, Any]):
        self.table_name = table_name
        self.values = values
        super().__init__(db_label=db_label)


class RemoveColumnOperation(Operation):
    def __init__(self, db_label: str, table_name: str, field_name: str):
        self.table_name = table_name
        self.field_name = field_name
        super().__init__(db_label=db_label)


class UnknownOperationException(Exception):
    pass
