from __future__ import annotations

import inspect
import os

from functools import reduce
from typing import Callable, Dict, List, Tuple

from .db.defaults import DefaultDatabases
from .db.databases import Database
from .handlers.contrib import welcome_handler
from .modules import Module
from .routers.utils import normalize_path
from .routers.route_map import build_routes
from .routers.defaults import DefaultRouter
from .requests.request import Request


class Application:
    # Application
    APP_PATH = "main:app"
    BASE_DIR = os.path.dirname(__file__)
    HOST = "127.0.0.1"
    PORT = 5000

    # Commands
    commands: Dict[str, Callable] = {}
    DEFAULT_COMMAND = "runserver"

    # Database
    databases: List[Database] = DefaultDatabases
    MIGRATIONS_TABLE_NAME = "sn_migrations"

    # Development
    DEBUG = True
    RELOAD_RUNSERVER = True

    # Logging
    LOG_LEVEL = "info"

    # Modules
    modules: List[Module] = []

    # Router
    router = DefaultRouter

    def __new__(cls):
        cls.APP_FILE = inspect.getfile(cls)
        cls.BASE_DIR = os.path.dirname(cls.APP_FILE)
        cls.MIGRATIONS_DIR = os.path.join(cls.BASE_DIR, "migrations")
        return super(Application, cls).__new__(cls)

    def __init__(self):
        self.models = reduce(lambda acc, m: acc + m.models, self.modules, [])
        self._route_map, self._dynamic_routes = build_routes(self.router)

    def get_request_handler(self, scope) -> Tuple[Callable, Request]:
        scope_path = normalize_path(scope["path"])

        # Attempt a lookup of static URLs
        if scope_path in self._route_map:
            request = Request(scope)
            return self._route_map[scope_path], request

        # Attempt a regex lookup of dynamic URLs (those with :param<type> items)
        for dynamic_route, handler in self._dynamic_routes:
            if dynamic_match := dynamic_route.match(scope_path):
                request = Request(scope, params=dynamic_match.groupdict())
                return handler, request

        # TODO: 404 handling
        request = Request(scope)
        return welcome_handler, request

    async def __call__(self, scope, receive, send):
        self.receive = receive
        assert scope["type"] == "http"

        request_handler, request = self.get_request_handler(scope)
        response = await request_handler(request)
        for message in response.get_messages():
            await send(message)
