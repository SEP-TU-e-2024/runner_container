"""
This module contains the CheckCommand class.
"""

from .command import Command


class CheckCommand(Command):
    """
    Command used to check the status of the runner.
    """
    
    def execute(self, args: dict):
        return {"status": "ok"}