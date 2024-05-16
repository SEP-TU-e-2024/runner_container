from settings import *

import docker
import time

class Runner():
    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_image, _ = self.docker_client.images.build(path=DOCKER_FILE_PARRENT_DIR)
        #self.docker_container = self.docker_client.containers.create(
        #    image=docker_image,
        #    mounts=[docker.types.Mount()])

    def run(self):
        container = self.docker_client.containers.run(image=self.docker_image, volumes={'stdout.txt':{'bind':'/target/stdout.txt','mode':'rw'}})
        print(container)
        

#----------------------------------------------------------------
# TESTING
#----------------------------------------------------------------
if __name__ == "__main__":
    r = Runner()
    r.run()