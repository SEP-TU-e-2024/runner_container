# Runner Container
Bare-bones Docker container that takes an executable and an evaluation library and outputs a full array of metrics, including execution time and quality of results

## How it works
The runner expects three folders to be mounted, `/library`, `/code` and `/metrics`. When running, it will automatically run `main.py` in the `/code` folder, using a specified library. Results will be output in a `.csv` (can/should be changed) file in `/results`.

The log shows the total and CPU time of the program.

## Progress
MVP requirements are achieved and the container runs without any issues. All implemented features seem to work.

# Some options:
Using container.logs(stream=True), this returns a blocking stream object where you can process output as they happen

Using named pipes: make pipes somewhere on your system (example: /tmp/pipe) and then mount these pipes to your docker container

Using devices: in docker.containers.run you can specify devicise the container has access to, you might be able to connect it to /dev/stdout
and /dev/stdin