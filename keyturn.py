import docker
import random
import string
import subprocess
import time
import json

docker_client = docker.from_env()
imagefile = "runner_container"
code_path = "/repository"

metrics_path = "~/metrics"


def generate_string(len):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(len))
    return password

#listen for web requests and unzip the received file in a clean working folder

def main():
    # listen for web requests
    # unzip the received file in a clean working folder
    # read and parse the metadata of the current problem
    metadata = open("metadata.json", "r")
    parsed_metadata = json.loads(metadata.read())
    time_limit = parsed_metadata["time_limit"]
    memory_limit = parsed_metadata["memory_limit"] + "m"

    # create a container and attach the relevant drives to the container
    problem_name = "default_problem"
    library_path = "~/problems"+problem_name+"/library"
    id = generate_string(12);
    container = docker_client.containers.run(
            image=imagefile,
            volumes={code_path: {'bind': '/code', 'mode': 'r'},
                     library_path: {'bind': '/library', 'mode': 'r'},
                     metrics_path: {'bind': '/metrics', 'mode': 'r'}},
            environment = ["TIMEID=" + id]
        )
    
    # set memory limit
    docker_client.container.update(mem_limit=memory_limit)

    # disconnect the container from the network when configuration is done
    while container.status != "exited":
        container_log = container.logs()
        if 'Network to be disabled' in container_log:
            docker_client.disconnect(container, force=True)
            break
    # listen for the container to finish executing, while also checking if it goes over the time limit
    while container.status != "exited":
        time.sleep(1)
        if (time.time() - container.attrs['State']['StartedAt']) > time_limit:
            container.stop()
            break
    # process the results to obtain scores for the answers, using the processor script
    proc = subprocess.Popen(["python3", "~/problems"+problem_name+"/processor.py", id], stdout=subprocess.PIPE)
    result = proc.stdout.read()
    # retrieve time metrics from the container
    # return the results to the web request

if __name__ == "__main__":
    main()