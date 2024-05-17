from settings import *

import os
import docker
from docker.types import Mount
import subprocess
import time

PIPE_STDOUT = '/tmp/test'

class Runner():
    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_image, _ = self.docker_client.images.build(path=DOCKER_FILE_PARRENT_DIR)

        self._setup_pipes()

    def _setup_pipes(self):
        if not os.path.exists(PIPE_STDOUT):
            os.mkfifo(PIPE_STDOUT)

    def run(self):
        mount = Mount(target='/tmp/test', source=PIPE_STDOUT, type='bind')
        container = self.docker_client.containers.run(image=self.docker_image, mounts=[mount], detach=True)

        validator = subprocess.Popen("python3 validator.py > /tmp/test", stdin=subprocess.PIPE, shell=True)

        for data  in container.logs(stream=True):
            print(f"runner: {data.decode()}")
            if validator.poll() == None:
                validator.communicate(input=data)

#----------------------------------------------------------------
# TESTING
#----------------------------------------------------------------
if __name__ == "__main__":
    r = Runner()
    r.run()