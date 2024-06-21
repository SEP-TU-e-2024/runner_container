"""
This module contains code used for creating and managing the containers created by the runner.
"""

import os
import random
import shutil
import time
from csv import DictReader
from enum import Enum
from logging import Logger
from os import path
from threading import Timer

import docker
import requests
from docker.types import Mount

from custom_logger import main_logger
from settings import (
    DOCKER_IMAGE,
    DOCKER_INSTANCES,
    DOCKER_RESULTS,
    DOCKER_SUBMISSION,
    DOCKER_VALIDATOR,
)


class Status(Enum):
    """
    Enum for the status of the container.
    """

    INITIALIZING = "initializing"
    """
    The container is initializing.
    """

    INITIALIZED = "initialized"
    """
    The container is initialized.
    """

    RUNNING = "running"
    """
    The container is running.
    """

    SUCCESS = "success"
    """
    The container has finished successfully.
    """

    TIMEOUT = "timeout"
    """
    An evaluation in the container timed out.
    """

    ERROR = "error"
    """
    An evaluation in the container errorred.
    """

class Container:
    id: str
    logger: Logger
    docker_client: docker.DockerClient
    container: docker.models.containers.Container
    mounts: list[Mount]
    time_limit: int
    status: Status = Status.INITIALIZING

    def __init__(self, submission_url: str, validator_url: str, benchmark_instances: dict[str, str], evaluation_settings: dict[str, int]):
        # Generate a random ID
        self.id = f"{random.randint(0, 0xffffffff):08x}"
        self.logger = main_logger.getChild(f"container-{self.id}")

        # Set up the Docker container
        self.docker_client = docker.from_env()
        self._config_mounts()
        self._setup_mount_content(DOCKER_SUBMISSION, {"submission.zip": submission_url})
        self._setup_mount_content(DOCKER_VALIDATOR, {"validator.zip": validator_url})
        self._setup_mount_content(DOCKER_INSTANCES, benchmark_instances)
        self.container = self.docker_client.containers.create(
            name=f"BenchLab_Runner_{self.id}",
            image=DOCKER_IMAGE,
            mounts=self.mounts,
            detach=True,
            auto_remove=True,
            # Add evaluation settings
            cpu_period=100000,
            cpu_quota=evaluation_settings["cpu"] * 100000,
            mem_limit=f"{evaluation_settings['memory']}m",
        )

        self.time_limit = evaluation_settings["time_limit"]
        self.status = Status.INITIALIZED

    def __del__(self):
        self.tidy()

    @staticmethod
    def build_image():
        """
        Build the Docker image for the runner.
        """
        main_logger.info("Building image")
        start_time = time.time()

        # Build image
        client = docker.from_env()
        client.images.build(path=".", tag=DOCKER_IMAGE, rm=True)

        main_logger.info(f"Image built, took {time.time() - start_time}s")

    def tidy(self):
        '''
        Remove the directory and all subdirectories corresponding to this container (based on `id`).
        '''
        if path.exists(self._folder()):
            shutil.rmtree(self._folder())

    def _folder(self, path: str = None):
        parts = [os.getcwd(), "containers", self.id]

        if path is not None:
            if path[0] == "/":
                path = path[1:]
            parts.append(path)

        return os.path.join(*parts)

    def _config_mounts(self):
        """
        Generate the mounts for the container, stored in `mounts` field.
        """

        # Create mounts for this directory
        for dir in [DOCKER_SUBMISSION, DOCKER_VALIDATOR, DOCKER_INSTANCES, DOCKER_RESULTS]:
            os.makedirs(self._folder(dir))

        # Define the mounts for the docker container
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
                target=DOCKER_INSTANCES,
                source=self._folder(DOCKER_INSTANCES),
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

    def _setup_mount_content(self, mounted_folder: str, file_to_url: dict[str, str]):
        for output_file, url in file_to_url.items():
            response = requests.get(url)
            
            file_path = self._folder(f"{mounted_folder}/{output_file}")

            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                self.logger.info(f"File downloaded succesfully from: {url}, filename: {file_path}")
            else:
                self.logger.info(f"Could not download file from: {url}, filename: {file_path}")
                raise Exception(f"Error could not download {output_file} from {url}")

    def _format_results(self):
        """
        Formats the results from the evaluation in simple dictionaries.
        """
        result = {}

        # Iterate over all benchmark instances
        for entry in os.listdir(self._folder(DOCKER_RESULTS)):
            results_folder = path.join(self._folder(DOCKER_RESULTS), entry)

            with open(path.join(results_folder, 'results.csv')) as file:
                csv_reader = DictReader(file)
                results = list(csv_reader)

            with open(path.join(results_folder, 'metrics.csv')) as file:
                csv_reader = DictReader(file)
                metrics = list(csv_reader)

            with open(path.join(results_folder, 'CPU_times.csv')) as file:
                csv_reader = DictReader(file)
                cpu_times = list(csv_reader)

            # Add some hardware metrics to the results
            results[0]["wall_time"] = float(cpu_times[0]["Wall time"])
            results[0]["user_time"] = float(cpu_times[0]["User time"])
            results[0]["system_time"] = float(cpu_times[0]["System time"])
            results[0]["max_ram_mb"] = float(cpu_times[0]["Max RAM(KB)"]) / 1000 # in MB

            data = {
                "results": results,
                "metrics": metrics,
                "cpu_times": cpu_times
            }

            result[entry] = data
        
        return result

    def run(self):
        """
        Run the container.

        Returns the formatted results of the container if successful, otherwise None.
        """
        self.logger.info("Running...")
        self.container.start()
        self.status = Status.RUNNING

        timer = Timer(self.time_limit, self.__timeout_stop)

        for data in self.container.logs(stream=True):
            self.logger.info(f"Docker: {data.decode()}")
            if data.decode().find("Starting the main code") != -1:
                self.__network_kill()
            if data.decode().find("Starting benchmark instance ") != -1:
                timer.cancel()
                timer = Timer(self.time_limit, self.__timeout_stop)
                timer.start()

        timer.cancel()

        # Update status
        if self.status != Status.TIMEOUT:
            exit_code = self.container.wait()["StatusCode"]
            if exit_code != 0:
                self.logger.error(f"Container exited with code {exit_code}")
                self.status = Status.ERROR
            else:
                self.status = Status.SUCCESS

        self.container.stop()
        if self.status == Status.SUCCESS:
            return self._format_results()
        
        return None
    
    def __timeout_stop(self):
        """
        Kill the container because of a timeout.
        """
        self.logger.info("Timeout reached, stopping container.")
        self.status = Status.TIMEOUT
        self.container.stop(timeout = 0)

    def __network_kill(self):
        """
        Remove the network connection when the main.py file is executed
        """
        for network in self.docker_client.networks.list():
            network.reload()
            container_connections = network.attrs.get('Containers', {})
            
            # Check if the container is connected to the current network
            if self.container.id in container_connections:
                network.disconnect(self.container)
                self.logger.info(f"Disconnected {self.container.name} from network {network.name}")


# ----------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------
# Run python3 -m http.server in local_testing
if __name__ == "__main__":
    Container.build_image()

    evaluation_settings = {
        "cpu": 1,
        "memory": 512,
        "time_limit": 1000,
    }

    benchmark_instances = {"instance1": "http://0.0.0.0:8001/ORTEC-VRPTW-ASYM-0bdff870-d1-n458-k35.txt"}

    c = Container(submission_url="http://0.0.0.0:8001/submission.zip",
                  validator_url="http://0.0.0.0:8001/validator.zip",
                  benchmark_instances=benchmark_instances,
                  evaluation_settings=evaluation_settings)
    output = c.run()

    print(repr(output))
    print(f'status: {c.status}')
