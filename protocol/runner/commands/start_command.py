from .command import Command


class StartCommand(Command):
    """
    Command used to check the status of the runner.
    """

    @staticmethod
    def execute(args: dict):
        return {"status": "ok"}
