from typing import Callable, List, Pattern, Tuple

from .dynamic_routes import path_to_regex
from .router import Router
from .route import Route
from .utils import normalize_path


def build_static_routes(router: Router) -> dict:
    route_map = {}
    for route in router.routes:
        path = normalize_path(route.path)
        if isinstance(route, Route):
            route_map[path] = route.handler
        elif isinstance(route, Router):
            nested_map = build_static_routes(route)
            for key, value in nested_map.items():
                full_key = f"{route.path}{key}"
                route_map[full_key] = value
    return route_map


DynamicRouteType = List[Tuple[Pattern[str], Callable]]


def build_routes(router: Router) -> Tuple[dict, DynamicRouteType]:
    route_map = build_static_routes(router)

    dynamic_routes: DynamicRouteType = []
    for key in route_map.copy():
        if ":" in key:
            regex = path_to_regex(key)
            dynamic_routes.append((regex, route_map[key]))
            del route_map[key]
    return route_map, dynamic_routes
