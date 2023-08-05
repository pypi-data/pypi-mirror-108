from stonehenge.db.databases import SQLite3Database

DefaultDatabases = [
    SQLite3Database(
        label="default",
        filename="dev.db",
    )
]
