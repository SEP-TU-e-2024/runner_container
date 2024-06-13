"""
This module contains the StartCommand class.
"""

from container import Container

from .command import Command


class StartCommand(Command):
    """
    The StartCommand class is used to start a container on the runner.
    """

    @staticmethod
    def execute(args: dict):
        if "submission" not in args or "validator" not in args:
            return {"status": 400}
        container = Container(submission_url=args["submission"], problem_url=args["validator"])
        res = container.run()
        return {"status": "ok", "results": res}
