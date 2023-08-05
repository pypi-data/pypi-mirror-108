from urllib.parse import urlparse, parse_qs


def parse_query(query_string: bytes) -> dict:
    """Return a dictionary containing URL query params

    Example:
        input [bytes]: b"foo=bar&foo=baz&hello=world"
        output [dict]: {'foo': ['bar', 'baz'], 'hello': ['world']}
    """
    query = query_string.decode("utf-8")
    url_query = f"?{query}"
    parsed = urlparse(url_query)
    return parse_qs(parsed.query)
