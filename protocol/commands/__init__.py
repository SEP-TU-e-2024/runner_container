from enum import Enum

from .check_command import CheckCommand


class Commands(Enum):
    # START = _StartCommand()
    # """
    # Starts a new task for the runner.
    # """

    # STOP = _StopCommand()
    # """
    # Stops a certain task of the runner.
    # """

    CHECK = CheckCommand()
    """
    Checks if the runner is still alive.
    """
