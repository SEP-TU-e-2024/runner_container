import threading


class Counter:
    def __init__(self) -> None:
        self.id = 0
        self.lock = threading.Lock()

    def generate(self):
        with self.lock:
            current_id = self.id
            self.id += 1
        return current_id
