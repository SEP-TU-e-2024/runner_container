from enum import Enum

from .check_command import CheckCommand
from .start_command import StartCommand


class Commands(Enum):
    START = StartCommand()
    CHECK = CheckCommand()
