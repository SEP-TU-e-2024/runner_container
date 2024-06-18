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
        if any(required not in args for required in ["submission", "validator", "settings", "instances"]):
            return {"status": 400}
        container = Container(submission_url=args["submission"], validator_url=args["validator"], settings=args["settings"], instances=args["instances"])
        res = container.run()
        return {"status": "ok", "results": res}
