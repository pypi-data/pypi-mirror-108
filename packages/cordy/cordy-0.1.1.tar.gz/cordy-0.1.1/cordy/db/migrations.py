from playhouse.migrate import migrate


class Migration:

    operations = [[], []]

    def __init__(self, migrator):
        self.migrator = migrator

    def _perform(self, operations):
        migrate(*operations)

    def migrate(self):
        operations = [
            getattr(self.migrator, op[0])(*op[1:])
            for op in self.operations[0]
        ]
        self._perform(operations)

    def reverse(self):
        operations = [
            getattr(self.migrator, op[0])(*op[1:])
            for op in self.operations[1]
        ]
        self._perform(operations)
