class UnappliedMigrationException(Exception):
    def __init__(self, filepath):
        msg = f'Unapplied migration for "{filepath}"'
        super().__init__(msg)
