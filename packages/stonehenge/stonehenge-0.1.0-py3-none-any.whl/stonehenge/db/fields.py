from typing import Any, Union

from stonehenge.db.columns import ColumnType


class Field:
    db_column_type: ColumnType

    def __init__(self, default: Any = None, null=False, primary_key=False):
        self.default = default
        self.primary_key = primary_key
        self.null = null


class CharField(Field):
    db_column_type: ColumnType = "VARCHAR"

    def __init__(
        self,
        max_length: int,
        default: Union[str, None] = None,
        null=False,
        primary_key=False,
    ):
        self.max_length = max_length
        super().__init__(default=default, null=null, primary_key=primary_key)


class DateTimeField(Field):
    db_column_type: ColumnType = "VARCHAR"

    def __init__(
        self, auto_now=False, auto_now_add=False, primary_key=False, null=False
    ):
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        super().__init__(default=None, null=null, primary_key=primary_key)


class ForeignKeyField(Field):
    db_column_type: ColumnType = "VARCHAR"

    def __init__(self, model_name: str, null=False, primary_key=False):
        self.model_name = model_name
        super().__init__(default=None, null=null, primary_key=primary_key)


class UUIDField(Field):
    db_column_type: ColumnType = "VARCHAR"


class BooleanField(Field):
    db_column_type: ColumnType = "INTEGER"


class IntegerField(Field):
    db_column_type: ColumnType = "INTEGER"
