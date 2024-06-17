"""
This module contains code used for creating and managing the containers created by the runner.
"""

import os
import random
import shutil
from csv import DictReader
from os import path

import docker
import requests
from docker.types import Mount

from custom_logger import main_logger
from settings import DOCKER_IMAGE, DOCKER_RESULTS, DOCKER_SUBMISSION, DOCKER_VALIDATOR


class Container:
    def __init__(self, submission_url: str, validator_url: str):
        self.id = f"{random.randint(0, 9999)}-{random.randint(0, 0xffffffff)}"
        self.logger = main_logger.getChild(f"container-{self.id}")

        self.docker_client = docker.from_env()
        self._config_mounts()
        self._setup_mount_content(submission_url, f"{DOCKER_SUBMISSION}/submission.zip")
        self._setup_mount_content(validator_url, f"{DOCKER_VALIDATOR}/validator.zip")
        self.container = self.docker_client.containers.create(
            image=DOCKER_IMAGE, mounts=self.mounts, detach=True
        )
        
    def __del__(self):
        # remove the directory and all subdirectories corresponding to this container (based on id)
        shutil.rmtree(self._folder())

    def _folder(self, path: str = None):
        if path:
            if path[0] == "/":
                path = path[1:]
            return os.path.join(os.getcwd(), self.id, path)
        return os.path.join(os.getcwd(), self.id)

    def _config_mounts(self):
        """
        Configures the mounts for the container.
        """
        
        # create mounts for this directory
        for dir in [DOCKER_SUBMISSION, DOCKER_VALIDATOR, DOCKER_RESULTS]:
            os.makedirs(self._folder(dir))

        # define the mounts for the docker container
        self.mounts = [
            Mount(
                target=DOCKER_SUBMISSION,
                source=self._folder(DOCKER_SUBMISSION),
                type="bind",
                read_only=True,
            ),
            Mount(
                target=DOCKER_VALIDATOR,
                source=self._folder(DOCKER_VALIDATOR),
                type="bind",
                read_only=True,
            ),
            Mount(
                target=DOCKER_RESULTS,
                source=self._folder(DOCKER_RESULTS),
                type="bind",
                read_only=False
            ),
        ]

    def _setup_mount_content(self, url: str, output_file: str):
        response = requests.get(url)
        
        file_path = self._folder(output_file)

        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            self.logger.info(f"File downloaded succesfully from: {url}, filename: {file_path}")
        else:
            self.logger.info(f"Could not download file from: {url}, filename: {file_path}")
            raise Exception(f"Error could not download {output_file} from {url}")

    # This function needs to be changed later when we add vlads code
    def _format_results(self):
        res_folder = self._folder(DOCKER_RESULTS)

        with open(path.join(res_folder, 'results.csv')) as file:
            csv_reader = DictReader(file)
            results = list(csv_reader)

        with open(path.join(res_folder, 'metrics.csv')) as file:
            csv_reader = DictReader(file)
            metrics = list(csv_reader)

        with open(path.join(res_folder, 'CPU_times.csv')) as file:
            csv_reader = DictReader(file)
            cpu_times = list(csv_reader)

        return {
            "results": results,
            "metrics": metrics,
            "cpu_times": cpu_times
        }

    def run(self):
        """
        Run the container.
        """
        self.logger.info("Running...")
        self.container.start()

        for data in self.container.logs(stream=True):
            self.logger.info(f"Docker: {data.decode()}")
        
        return self._format_results()


# ----------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------
# Run python3 -m http.server in local_testing
if __name__ == "__main__":
    c = Container(submission_url="http://0.0.0.0:8000/submission.zip", validator_url="http://0.0.0.0:8000/validator.zip")
    out = c.run()
    print(repr(out))
