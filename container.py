"""
This module contains code used for creating and managing the containers created by the runner.
"""

import os
import shutil
import random

import docker
from docker.types import Mount

from settings import DOCKER_IMAGE, DOCKER_RESULTS, DOCKER_SUBMISSION, DOCKER_VALIDATOR


class Container:
    dirs = [DOCKER_SUBMISSION, DOCKER_VALIDATOR, DOCKER_RESULTS]

    def __init__(self, submission: str, problem: str):
        self.submission = submission
        self.problem = problem

        self.id = f"{random.randint(0, 9999)}-{random.randint(0, 0xffffffff)}"

        self.docker_client = docker.from_env()
        self._config_mounts()
        self._setup_mounts_content()
        self.container = self.docker_client.containers.create(
            image=DOCKER_IMAGE, mounts=self.mounts, detach=True
        )
        
    def __del__(self):
        # remove the directory and all subdirectories corresponding to this container (based on id)
        shutil.rmtree(f"{os.getcwd()}/{self.id}")

    def _config_mounts(self):
        """
        Configures the mounts for the container.
        """
        cwd = os.getcwd()
        
        # create mounts for this directory
        for dir in self.dirs:
            os.makedirs(f"{cwd}/{self.id}{dir}")

        # define the mounts for the docker container
        self.mounts = [
            Mount(
                target=DOCKER_SUBMISSION,
                source=f"{cwd}/{self.id}{DOCKER_SUBMISSION}",
                type="bind",
                read_only=True,
            ),
            Mount(
                target=DOCKER_VALIDATOR,
                source=f"{cwd}/{self.id}{DOCKER_VALIDATOR}",
                type="bind",
                read_only=True,
            ),
            Mount(
                target=DOCKER_RESULTS,
                source=f"{cwd}/{self.id}{DOCKER_RESULTS}",
                type="bind",
                read_only=False
            ),
        ]

    def _setup_mounts_content(self):
        pass

    def run(self, submission, validator):
        """
        Run the container.
        """
        print("Running...")
        self.container.start()

        for data in self.container.logs(stream=True):
            print(f"{data.decode()}", end="")


# ----------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------
if __name__ == "__main__":
    c = Container()
    c.run()
