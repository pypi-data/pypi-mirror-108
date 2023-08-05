import sys
from typing import Callable, Dict
from stonehenge.application import Application
from stonehenge.db.commands import makemigrations, migrate
from stonehenge.server.commands import runserver


class UnknownCommandException(Exception):
    pass


def run(app: Application):
    base_commands = [
        makemigrations,
        migrate,
        runserver,
    ]
    commands: Dict[str, Callable] = {f.__name__: f for f in base_commands}
    commands.update(app.commands)
    command_name = app.DEFAULT_COMMAND if len(sys.argv) < 2 else sys.argv[1]
    try:
        command = commands[command_name]
    except KeyError:
        raise UnknownCommandException(command_name)
    command(app)
