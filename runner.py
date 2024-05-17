from settings import *

import os
import docker
from docker.types import Mount
import subprocess
import time

PIPE_STDIN = '/tmp/stdin'

class Runner():
    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_image, _ = self.docker_client.images.build(path=DOCKER_FILE_PARRENT_DIR)

        self._setup_pipes()

    def _setup_pipes(self):
        if not os.path.exists(PIPE_STDIN):
            os.mkfifo(PIPE_STDIN)

    def run(self):
        mount = Mount(target=PIPE_STDIN, source=PIPE_STDIN, type='bind')
        container = self.docker_client.containers.run(image=self.docker_image, mounts=[mount], detach=True)

        validator = subprocess.Popen(f"python3 validator.py > {PIPE_STDIN}", stdin=subprocess.PIPE, shell=True)

        print("Start demo")

        for data in container.logs(stream=True):
            print(f"runner: {data.decode()}")
            if validator.poll() == None:
                validator.stdin.write(data)
                validator.stdin.flush()

#----------------------------------------------------------------
# TESTING
#----------------------------------------------------------------
if __name__ == "__main__":
    r = Runner()
    r.run()