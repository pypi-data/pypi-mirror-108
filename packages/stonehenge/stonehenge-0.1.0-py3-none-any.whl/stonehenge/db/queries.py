import sqlite3

from typing import Tuple


def get_single_field_from_db(table_name, id, field_name):
    # Conduct query
    query_str = "SELECT %s FROM %s WHERE id='%s'"
    params = (field_name, table_name, id)
    result = run_query(query_str, params)
    return result


def run_query(
    query_str: str, params: Tuple[str, ...], db_name="example.db", engine="sqlite3"
):
    """Conduct a query against the provided database.

    TODO: Support engines other than mysql
    """
    if engine != "sqlite3":
        raise NotImplementedError("Databases other than sqlite3 not yet supported")

    con = sqlite3.connect(db_name)
    try:
        with con:
            cur = con.cursor()
            cur.execute(query_str % params)
        return cur
    finally:
        con.close()
