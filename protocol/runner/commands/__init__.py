from enum import Enum

from .check_command import CheckCommand


class Commands(Enum):
    CHECK = CheckCommand()