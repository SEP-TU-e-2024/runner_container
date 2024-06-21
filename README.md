# Runner Container
This contains the library based implementation.
The submitted code is run in the Docker container and calls the library, which will also run in the container.
Then the library will write its results to a file.

## `.env` setup
```
JUDGE_HOST = "localhost"
JUDGE_PORT = "12345"
JUDGE_CONNECTION_RETRY_WAIT = "5"
```

## Start Files
To start the Judge Runner including the protocol, use `runner.py`.

For development purposes, you can also run this stand-alone with `container.py`. Do make sure that you run a webserver in `local_testing` at the same time using `./run.sh <problem name>`, where `<problem name>` is 'TestProblem' or 'VRPTW'.
