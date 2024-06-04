"""
Container CPU and memory usage tracker thread.
"""
import docker
from time import sleep
from time import time
from settings import DOCKER_RESULTS, DOCKER_TIMEOUT

def profiler(docker_container):
    #open the file to write the stats
    file_path = f"{DOCKER_RESULTS}/metrics.csv"
    file = open(file_path, "w")

    start_time = time()

    while docker_container.status == "running":

        stats = docker_container.stats(stream=False)
        file.write(f"CPU: {stats['cpu_stats']['cpu_usage']['total_usage']}\n")
        
        if time() - start_time > DOCKER_TIMEOUT:
            docker_container.stop()
            break

        sleep(1)
        
    file.close()
        

