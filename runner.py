from settings import *

import os
import docker
from docker.types import Mount
import subprocess

PIPE_STDOUT = '/tmp/test'

class Runner():
    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_image, _ = self.docker_client.images.build(path=DOCKER_FILE_PARRENT_DIR)

        #self._setup_pipes()

    def _setup_pipes(self):
        if not os.path.exists(PIPE_STDOUT):
            os.mkfifo(PIPE_STDOUT)

    def run(self):
        #mount = Mount(target='/target/test', source=PIPE_STDOUT, type='npipe')
        #container = self.docker_client.containers.run(image=self.docker_image, mounts=[mount], detach=True)
        container = self.docker_client.containers.run(image=self.docker_image, detach=True)

        #print("container done")
        #subprocess.Popen("echo bruh > /tmp/test", shell=True)
        #subprocess.Popen("cat /tmp/test", shell=True)
        #print("subprocess run")

        #print(container.logs().decode())
        for r in container.logs(stream=True):
            print(r)
        

#----------------------------------------------------------------
# TESTING
#----------------------------------------------------------------
if __name__ == "__main__":
    r = Runner()
    r.run()