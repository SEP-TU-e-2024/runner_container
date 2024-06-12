"""
This module contains the InfoCommand class.
"""

import platform

from .command import Command


class InfoCommand(Command):
    """
    Command used to get the machine name of the runner.
    """

    @staticmethod
    def execute(args: dict):
        return {"machine_name": platform.node()}
