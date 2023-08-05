from typing import Dict, Any, List, TypeVar, Type

from .fields import Field, UUIDField
from .queries import get_single_field_from_db


T = TypeVar("T", bound="DBQueryMixin")


class ModelBase(type):
    """Metaclass for tracking which fields on the model are database fields

    This allows for instances of the model to access the value of a field via instance.field,
    while allowing the class to retrieve the field object as Class.field. This is done
    in conjunction with the overwritten __getattribute__ field on the base model class.

    Examples:
        ```
        class BlogPost(models.Model):
            title = fields.CharField()

        post = BlogPost()

        BlogPost.title // <stonehenge.db.fields.CharField>
        post.title // <string>
        ```
    """

    def __new__(cls, name, bases, attrs):
        attrs["_db_fields"] = {k: v for k, v in attrs.items() if isinstance(v, Field)}
        result = super().__new__(cls, name, bases, attrs)
        return result


class DBQueryMixin:
    id = UUIDField()
    _db_fields: Dict[str, Field] = {}
    _db_field_values: Dict[str, Any] = {}
    _db_label = "default"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_from_db()

    @classmethod
    def find(cls: Type[T], **kwargs) -> T:
        return cls()

    @classmethod
    def find_values(cls: Type[T], **kwargs) -> dict:
        return {}

    @classmethod
    def filter(cls: Type[T], **kwargs) -> List[T]:
        return [cls()]

    @classmethod
    def _get_db_name(cls) -> str:
        return cls.__name__.lower()

    def refresh_from_db(self, fields_to_update=None):
        """Update internal field values from database"""
        field_names = fields_to_update or self._db_fields.keys()
        for field_name in field_names:
            value = get_single_field_from_db(
                self.__class__._get_db_name(), self.id, field_name
            )
            self._db_field_values[field_name] = value


class Model(DBQueryMixin, metaclass=ModelBase):
    def __getattribute__(self, name: str):
        if name == "_db_fields" or name not in self._db_fields:
            return super().__getattribute__(name)
        return self._db_field_values[name]
