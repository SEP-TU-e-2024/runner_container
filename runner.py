from settings import *

import docker
from docker.types import Mount
import os

class Runner():
    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_image, _ = self.docker_client.images.build(path=DOCKER_FILE_PARRENT_DIR) # this is temp, for testing its easier to just build the image every time
        print("Done building image")

        self._config_mounts()
        self.container = self.docker_client.containers.create(image=self.docker_image, mounts=self.mounts, detach=True)
    
    def _config_mounts(self):
        cwd = os.getcwd()
        self.mounts = [Mount(target=DOCKER_SUBMISSION, source=f'{cwd}{DOCKER_SUBMISSION}', type="bind", read_only=True),
                       Mount(target=DOCKER_VALIDATOR, source=f'{cwd}{DOCKER_VALIDATOR}', type="bind", read_only=True)]

    def run(self):
        self.container.start()

        print(self.container.logs().decode())

#----------------------------------------------------------------
# TESTING
#----------------------------------------------------------------
if __name__ == "__main__":
    r = Runner()
    r.run()