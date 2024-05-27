import logging
import os

"""
The main logger to be used by the program.
"""

main_logger: logging.Logger = logging.getLogger("runner")

if not os.path.exists("logs"):
    os.makedirs("logs")

# Allow all log levels
main_logger.setLevel(logging.DEBUG)


def setup():
    global main_logger

    formatter_c = logging.Formatter(
        "%(asctime)s  [\033[93m%(pathname)s:%(lineno)d\033[0m]  %(levelname)s: %(message)s"
    )
    # formatter_f = logging.Formatter(
    #     "%(asctime)s  [%(pathname)s:%(lineno)d]  %(levelname)s: %(message)s"
    # )

    # Add console log handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter_c)
    main_logger.addHandler(console_handler)


setup()
