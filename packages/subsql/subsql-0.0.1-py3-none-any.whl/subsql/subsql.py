from functools import partialmethod
import os

class SubSQL:

    def __init__(self, connection, driver=None, modifiers=None, root=''):
        self.conn = connection
        self.driver = driver
        self.modifiers = modifiers if modifiers else dict()
        self.root = root

    def load(self, path, modifiers=None):
        errors, commands = self.driver.parse(os.path.normpath(os.path.join(self.root, path)))

        if (errors):
            raise ValueError("\n".join([str(e) for e in errors]))

        properties = {
            "conn": self.conn,
            "modifiers": modifiers if modifiers else self.modifiers,
        }

        for command in commands:
            properties[command.name] = partialmethod(self.driver.execute, command)

        klass = type("", (), properties)
        instance = klass()

        return instance
