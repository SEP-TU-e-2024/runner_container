import os

import docker
from docker.types import Mount

from settings import DOCKER_FILE_PARRENT_DIR, DOCKER_RESULTS, DOCKER_SUBMISSION, DOCKER_VALIDATOR


class Container:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_image, _ = self.docker_client.images.build(
            path=DOCKER_FILE_PARRENT_DIR
        )  # this is temp, for testing its easier to just build the image every time
        print("Done building image")

        self._config_mounts()
        self.container = self.docker_client.containers.create(
            image=self.docker_image, mounts=self.mounts, detach=True
        )
        # self.container = self.docker_client.containers.create(image=DOCKER_IMAGE, mounts=self.mounts, detach=True)

    def _config_mounts(self):
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
