from typing import List, Type

from .defaults import DefaultModules
from stonehenge.db.models import Model


class Module:
    models: List[Type[Model]] = []


__all__ = ["DefaultModules", "Module"]
