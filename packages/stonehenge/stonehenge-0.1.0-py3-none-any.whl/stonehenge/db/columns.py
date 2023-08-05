from __future__ import annotations
from typing import Literal, Union

ColumnType = Union[
    Literal["VARCHAR"],
    Literal["INTEGER"],
    Literal["FLOAT"],
    Literal["BOOL"],
]


class DBColumn:
    def __init__(
        self,
        column_type: ColumnType,
        field_name: str,
        null: bool,
        length: Union[int, None] = None,
        primary_key=False,
    ):
        self.length = length
        self.field_name = field_name
        self.null = null
        self.column_type = column_type
        self.primary_key = primary_key

    def __str__(self):
        return f"""Column ({self.field_name})
          column_type: {self.column_type}
          null: {self.null}
          primary_ley: {self.primary_key}
      """

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @classmethod
    def from_json(cls, data) -> DBColumn:
        return DBColumn(**data)

    @classmethod
    def from_sqlite3_pragma(cls, row) -> DBColumn:
        params = {
            "column_type": row[2],
            "field_name": row[1],
            "null": bool(row[3]),
        }
        if default := row[4]:
            params["default"] = default
        if row[5]:
            params["primary_key"] = True
        return DBColumn(**params)

    def to_json(self):
        return self.__dict__

    def get_sql_descriptor(self) -> str:
        """Return a snippet of text describing the column for use in a SQL operation

        Examples:
            first_name VARCHAR(255)
            Age int
        """
        if self.column_type == "BOOL":
            return f"{self.field_name} TINYINT"
        primary_key_param = "PRIMARY KEY" if self.primary_key else ""
        length_param = f"({self.length})" if self.length else ""
        column_param = f"{self.column_type}{length_param}"
        parts = [
            self.field_name,
            column_param,
            primary_key_param,
        ]
        return " ".join([f for f in parts if f])
