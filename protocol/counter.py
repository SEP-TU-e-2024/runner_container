"""
This module contains the Counter class.
"""

import threading


class Counter:
    """
    The counter class can be used to generate unique message IDs by incrementing a counter.
    """

    count: int
    start: int

    def __init__(self, start: int = 0) -> None:
        self.count = start
        self.lock = threading.Lock()

    def generate(self):
        """
        This method retruns the generted unique messaage ID by incrementing a counter. This method is thread-safe.
        """
        with self.lock:
            current_count = self.count
            self.count += 1

        return current_count
