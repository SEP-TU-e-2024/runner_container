# Runner Container
Bare-bones Docker container that takes an executable and an evaluation library and outputs a full array of metrics, including execution time and quality of results

## How it works
The runner expects three folders to be mounted, `/library`, `/code` and `/results`. When running, it will automatically run `main.py` in the `/code` folder, using a specified library. Results will be output in a `.csv` file in `/results`.

The log shows the total and CPU time of the program.