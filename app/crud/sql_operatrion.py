import sqlparse

def detect_sql_operation(query: str) -> str:
    parsed = sqlparse.parse(query)
    if not parsed:
        return "unknown"

    stmt = parsed[0]
    token_type = stmt.get_type().lower()
    return token_type