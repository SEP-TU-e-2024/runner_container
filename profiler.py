"""
Container CPU and memory usage tracker thread.
"""
import docker
from time import sleep
from settings import DOCKER_RESULTS

def profiler(docker_container):
    #open the file to write the stats
    file_path = f"{DOCKER_RESULTS}/metrics.csv"
    file = open("stats.txt", "w")

    while docker_container.status == "running":
        stats = docker_container.stats(stream=False)
        file.write(f"CPU: {stats['cpu_stats']['cpu_usage']['total_usage']}\n")
        sleep(1)