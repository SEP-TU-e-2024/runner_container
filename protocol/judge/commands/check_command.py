from .command import Command


class CheckCommand(Command):
    @staticmethod
    def response(response: dict):

        if response["status"] is None:
            raise ValueError("Received message with missing status!")

        status = response["status"]

        if status != "ok":
            raise ValueError(f'Unexpected respone! Expected "ok" and got "{status}"')
