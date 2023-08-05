from stonehenge.auth import AuthModule
from stonehenge.db import DatabaseModule
from stonehenge.server import ServerModule

DefaultModules = [
    AuthModule(),
    DatabaseModule(),
    ServerModule(),
]
