import docker
import random
import string

docker_client = docker.from_env()
imagefile = "runner_container"
code_path = "/repository"
library_path = "/library"
metrics_path = "/metrics"


def generate_string(len):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(len))


#listen for web requests and unzip the received file in a clean working folder

def main():
    # listen for web requests
    # unzip the received file in a clean working folder
    # create a container and attach the relevant drives to the container
    id = generate_string(12);
    container = docker_client.containers.run(
            image=imagefile,
            volumes={code_path: {'bind': '/code', 'mode': 'r'},
                     library_path: {'bind': '/library', 'mode': 'r'},
                     metrics_path: {'bind': '/metrics', 'mode': 'r'}},
            environment = ["TIMEID=" + id]
        )
    
    while container.status != "exited":
        container_log = container.logs()
        if 'Network to be disabled' in container_log:
            docker_client.disconnect(container, force=True)
            break
    # listen for the container to finish
    # retrieve the results from the container
    # return the results to the web request

if __name__ == "__main__":
    main()