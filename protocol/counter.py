"""
This module contains the Counter class.
"""

import threading


class Counter:
    """
    The counter class can be used to generate unique messaage IDs by incrementing a counter.
    """

    def __init__(self, start: int = 0) -> None:
        self.id = start
        self.lock = threading.Lock()

    def generate(self):
        """
        This method retruns the generted unique messaage ID by incrementing a counter. This method is thread-safe.
        """
        with self.lock:
            current_id = self.id
            self.id += 1
        return current_id
