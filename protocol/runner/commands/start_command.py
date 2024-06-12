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
        container = Container()
        container.run()
        return {"status": "ok", "result": "abcd"}
