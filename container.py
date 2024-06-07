"""
This module contains code used for creating and managing the containers created by the runner.
"""

import os
import docker
from docker.types import Mount
from time import time

from custom_logger import main_logger
from settings import DOCKER_FILE_PARRENT_DIR, DOCKER_RESULTS, DOCKER_SUBMISSION, DOCKER_VALIDATOR, DOCKER_TIMEOUT

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

    def _profiler(self):
    #open the file to write the stats

        while self.container.status == "running":

            start_time = time()
            if time() - start_time > DOCKER_TIMEOUT:
                self.container.stop()
                break


        
    def _config_mounts(self):
        """
        Configures the mounts for the container.
        """
        
        cwd = os.getcwd()
        self.mounts = [
            Mount(
                target=DOCKER_SUBMISSION,
                source=f"{cwd}{DOCKER_SUBMISSION}",
                type="bind",
                read_only=True,
            ),
            Mount(
                target=DOCKER_VALIDATOR,
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

        # start the profiler thread
        # thread = Thread(target = self._profiler)
        # thread.start()

        for data in self.container.logs(stream=True):
            logger.debug(f"{data.decode()}")

# ----------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------
if __name__ == "__main__":
    c = Container()
    c.run()
