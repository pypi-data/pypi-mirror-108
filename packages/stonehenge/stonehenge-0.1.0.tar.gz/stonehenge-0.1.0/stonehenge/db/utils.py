from typing import Type

from stonehenge.application import Application
from stonehenge.db.databases import Database
from stonehenge.db.exceptions import DatabaseNotFound
from stonehenge.db.models import Model


def get_database_for_model(app: Application, model: Type[Model]) -> Database:
    """Return the database to use for the provided models

    This is based on the _db_label attribute of the model. Set to `default` for most models.
    """
    for database in app.databases:
        if database.label == model._db_label:
            return database
    model_name = model.__name__
    label = model._db_label
    raise DatabaseNotFound(
        f"Missing database for model {model_name} with DB label {label}"
    )
