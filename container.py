"""
This module contains code used for creating and managing the containers created by the runner.
"""

import os
import shutil
import random
import requests

import docker
from docker.types import Mount
from custom_logger import main_logger

from settings import DOCKER_IMAGE, DOCKER_RESULTS, DOCKER_SUBMISSION, DOCKER_VALIDATOR


class Container:
    def __init__(self, submission_url: str, problem_url: str):
        self.id = f"{random.randint(0, 9999)}-{random.randint(0, 0xffffffff)}"
        self.logger = main_logger.getChild(f"container-{self.id}")

        self.docker_client = docker.from_env()
        self._config_mounts()
        self._setup_mount_content(submission_url, f"{DOCKER_SUBMISSION}/submission.zip")
        self._setup_mount_content(problem_url, f"{DOCKER_VALIDATOR}/validator.zip")
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
        for dir in [DOCKER_SUBMISSION, DOCKER_VALIDATOR, DOCKER_RESULTS]:
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

    def _setup_mount_content(self, url: str, output_file: str):
        response = requests.get(url)
        
        file_path = f"{os.getcwd()}/{self.id}{output_file}"

        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            self.logger.info(f"File downloaded succesfully from: {url}, filename: {file_path}")
        else:
            self.logger.info(f"Could not download file from: {url}, filename: {file_path}")
            raise Exception(f"Error could not download {output_file} from {url}")

    def run(self):
        """
        Run the container.
        """
        self.logger.info("Running...")
        self.container.start()

        for data in self.container.logs(stream=True):
            print(f"{data.decode()}", end="")


# ----------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------
if __name__ == "__main__":
    c = Container()
    c.run()
