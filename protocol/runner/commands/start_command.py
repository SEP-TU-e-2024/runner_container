"""
This module contains the StartCommand class.
"""

from container import Container

from .command import Command


class StartCommand(Command):
    """
    The StartCommand class is used to start a container on the runner.
    """

    def execute(self, args: dict):
        submission_url = args["submission"]
        validator_url = args["validator"]

        # TODO: use URLs above, and get and send result
        print(f"Starting container with submission: {submission_url} and validator: {validator_url}")
        container = Container()
        container.run()

        return {"status": "ok", "result": "abcd"}
