from .command import Command


class CheckCommand(Command):
    @staticmethod
    def response(message: dict):
        if message["status"] is None:
            raise ValueError("Received message with missing status!")

        status = message["status"]

        if status != "ok":
            raise ValueError(f'Unexpected respone! Expected "ok" and got "{status}"')
