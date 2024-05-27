"""
This module is used for testing the connection between the judge and a runner (or possibly multiple ones).
"""

import threading
from time import sleep

import judge
import main


def test():
    judge_thread = threading.Thread(target=judge.main)
    judge_thread.start()
    sleep(2)
    runner_thread = threading.Thread(target=main.main)
    runner_thread.start()

    runner_thread.join()
    judge_thread.join()


if __name__ == "__main__":
    test()
