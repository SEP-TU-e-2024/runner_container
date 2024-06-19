"""
This module contains code used for creating and managing the containers created by the runner.
"""

import os
import random
import shutil
from csv import DictReader
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
    REQUIRED_SETTINGS,
)


class Container:
    def __init__(self, submission_url: str, validator_url: str, instances: dict[str, str], settings: dict[str, int]):
        if any(required not in settings for required in REQUIRED_SETTINGS):
            raise ValueError(f"Settings: {settings} does not contain the required fields")

        self.id = f"{random.randint(0, 9999)}-{random.randint(0, 0xffffffff)}"
        self.logger = main_logger.getChild(f"container-{self.id}")

        self.docker_client = docker.from_env()
        self._config_mounts()
        self._setup_mount_content(DOCKER_SUBMISSION, {"submission.zip": submission_url})
        self._setup_mount_content(DOCKER_VALIDATOR, {"validator.zip": validator_url})
        self._setup_mount_content(DOCKER_INSTANCES, instances)
        self.container = self.docker_client.containers.create(
            image=DOCKER_IMAGE, mounts=self.mounts, detach=True,
            cpu_period=100000, cpu_quota=settings["cpu"] * 100000, mem_limit=f"{settings['memory']}m",
        )
        self.stop_timer = Timer(settings["time_limit"], self.__timeout_stop)
        
    def __del__(self):
        self._tidy()

    def _tidy(self):
        '''
        remove the directory and all subdirectories corresponding to this container (based on id)
        '''
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
        for dir in [DOCKER_SUBMISSION, DOCKER_VALIDATOR, DOCKER_INSTANCES, DOCKER_RESULTS]:
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

    # This function needs to be changed later when we add vlads code
    def _format_results(self):
        result = {}

        for entry in os.listdir(self._folder(DOCKER_RESULTS)):
            res_folder = path.join(self._folder(DOCKER_RESULTS), entry)

            with open(path.join(res_folder, 'results.csv')) as file:
                csv_reader = DictReader(file)
                results = list(csv_reader)

            with open(path.join(res_folder, 'metrics.csv')) as file:
                csv_reader = DictReader(file)
                metrics = list(csv_reader)

            with open(path.join(res_folder, 'CPU_times.csv')) as file:
                csv_reader = DictReader(file)
                cpu_times = list(csv_reader)

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
        """
        self.logger.info("Running...")
        self.stop_timer.start()
        self.container.start()

        for data in self.container.logs(stream=True):
            self.logger.info(f"Docker: {data.decode()}")
            if (data.decode().find("Starting the main code") != -1):
                self.__network_kill()

        self.stop_timer.cancel()
        self.container.stop()
        return self._format_results()
    
    def __timeout_stop(self):
        """
        Kill the container.
        """
        self.logger.info("Timeout reached. Stopping container.")
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
                print(f"Disconnected {self.container.name} from network {network.name}")
        


# ----------------------------------------------------------------
# TESTING
# ----------------------------------------------------------------
# Run python3 -m http.server in local_testing
if __name__ == "__main__":
    settings = {
        "cpu": 1,
        "memory": 512,
        "time_limit": 20,
    }
    instances = {
        "instance1": "http://0.0.0.0:8000/instance1.txt",
        "instance2": "http://0.0.0.0:8000/instance2.txt"
    }
    c = Container(submission_url="http://0.0.0.0:8000/submission.zip", validator_url="http://0.0.0.0:8000/validator.zip", instances=instances, settings=settings)
    out = c.run()
    print(repr(out))
