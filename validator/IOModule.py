import csv
import os

import psutil


class IOModule:
    OUTPUT_FILE = "/results/results.csv"
    PERFORMANCE_ATTRS = ["cpu_times", "memory_full_info"]

    def _score(self) -> dict:
        return {'score':0}

    def __del__(self) -> None:
        """Function to evaluate inputs against expected answers and write the score to a csv file."""

        # Get the metrics: performance & problem specific metrics
        current_process = psutil.Process(os.getpid())
        metrics = {**current_process.as_dict(attrs=self.PERFORMANCE_ATTRS), **self._score()}

        with open(self.OUTPUT_FILE, "+w") as f:
            dict_writer = csv.DictWriter(f, metrics.keys())
            dict_writer.writeheader()
            dict_writer.writerows([metrics])