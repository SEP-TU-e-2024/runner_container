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
        if any(required not in args for required in ["submission_url", "validator_url", "evaluation_settings", "benchmark_instances"]):
            return {"status": "error"}
        container = Container(submission_url=args["submission_url"], validator_url=args["validator_url"], instances=args["benchmark_instances"], settings=args["evaluation_settings"])
        res = container.run()
        return {"status": "ok", "results": res}
