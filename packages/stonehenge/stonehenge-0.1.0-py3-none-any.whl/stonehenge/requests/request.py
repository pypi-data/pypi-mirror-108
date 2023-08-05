from .utils import parse_query


class Request:
    def __init__(self, scope, params={}):
        self.params = params
        self.query = parse_query(scope["query_string"])
        self.scope = scope
