import os
import time

import docker
from docker.types import Mount

from settings import DOCKER_FILE_PARRENT_DIR, DOCKER_RESULTS, DOCKER_SUBMISSION, DOCKER_VALIDATOR, DOCKER_TIMEOUT, DOCKER_MEMORY, DOCKER_CPUS


class Runner():
    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_image, _ = self.docker_client.images.build(path=DOCKER_FILE_PARRENT_DIR) # this is temp, for testing its easier to just build the image every time
        print("Done building image")

        self._config_mounts()
        self.container = self.docker_client.containers.create(image=self.docker_image, mounts=self.mounts, detach=True)
        self._config_resources()
        #self.container = self.docker_client.containers.create(image=DOCKER_IMAGE, mounts=self.mounts, detach=True)
    
    def _config_mounts(self):
        cwd = os.getcwd()
        self.mounts = [Mount(target=DOCKER_SUBMISSION, source=f'{cwd}{DOCKER_SUBMISSION}', type="bind", read_only=True),
                       Mount(target=DOCKER_VALIDATOR, source=f'{cwd}{DOCKER_VALIDATOR}', type="bind", read_only=True),
                       Mount(target=DOCKER_RESULTS, source=f'{cwd}{DOCKER_RESULTS}', type="bind", read_only=False)]
        
    def _config_resources(self):
        self.container.update(mem_limit=DOCKER_MEMORY, cpus=DOCKER_CPUS)

    def run(self):
        print("Running...")
        self.container.start()

        start_time = time.time()
        for data in self.container.logs(stream=True):
            print(f"{data.decode()}", end='')
            if (time.time() - start_time) > DOCKER_TIMEOUT:
                self.container.stop()
                break


#----------------------------------------------------------------
# TESTING
#----------------------------------------------------------------
if __name__ == "__main__":
    r = Runner()
    r.run()