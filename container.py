"""
This module contains code used for creating and managing the containers created by the runner.
"""

import os

import docker
from docker.types import Mount

from custom_logger import main_logger
from settings import (
    DOCKER_BASE,
    DOCKER_FILE_PARRENT_DIR,
    DOCKER_RESULTS,
    DOCKER_SUBMISSION,
    DOCKER_VALIDATOR,
)

logger = main_logger.getChild("container")


class Container:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_image, _ = self.docker_client.images.build(
            path=DOCKER_FILE_PARRENT_DIR
        )  # this is temp, for testing its easier to just build the image every time
        
        logger.info("Done building image")

        self._config_mounts()
        self.container = self.docker_client.containers.create(
            image=self.docker_image, mounts=self.mounts, detach=True
        )

    def _config_mounts(self):
        """
        Configures the mounts for the container.
        """
        
        cwd = os.getcwd()
        self.mounts = [
            Mount(
                target=f"{DOCKER_BASE}{DOCKER_SUBMISSION}",
                source=f"{cwd}{DOCKER_SUBMISSION}",
                type="bind",
                read_only=True,
            ),
            Mount(
                target=f"{DOCKER_BASE}{DOCKER_VALIDATOR}",
                source=f"{cwd}{DOCKER_VALIDATOR}",
                type="bind",
                read_only=True,
            ),
            Mount(
                target=DOCKER_RESULTS, source=f"{cwd}{DOCKER_RESULTS}", type="bind", read_only=False
            ),
        ]

    def run(self):
        """
        Run the container.
        """
        logger.info("Running...")
        self.container.start()

        for data in self.container.logs(stream=True):
            logger.debug(f"{data.decode()}")


# ----------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------
if __name__ == "__main__":
    c = Container()
    c.run()
