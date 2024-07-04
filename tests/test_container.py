from random import randrange

import docker

from container import Container, Status
from settings import DOCKER_IMAGE

from .util import http_server

CORRECT_SUBMISSION_PY = '''
from validator.validator import Validator

val = Validator()

total = 0

while True:
    n = val.obtain_data()
    print('got', n)
    if n == None:
        break
    total += n

print('total', total)
val.push_data(total)
'''

TIMEOUT_SUBMISSION_PY = '''
from validator.validator import Validator
from time import sleep

val = Validator()

total = 0

sleep(10)

while True:
    n = val.obtain_data()
    print('got', n)
    if n == None:
        break
    total += n

print('total', total)
val.push_data(total)
'''

ERROR_SUBMISSION_PY = '''
from validator.validator import Validator

val = Validator()

total = 0

raise ValueError()

while True:
    n = val.obtain_data()
    print('got', n)
    if n == None:
        break
    total += n

print('total', total)
val.push_data(total)
'''

VALIDATOR_PY = '''
class Validator():
    OUTPUT_FILE = "/results/results.csv"

    def __init__(self):
        self.reward = 0

        with open('instances/instance', 'r') as f:
            lines = f.readlines()
            self.right_answer = int(lines[0])
            self.numbers = [int(n) for n in lines[1:]]

    def obtain_data(self) -> int:
        if len(self.numbers) == 0:
            return None
        return self.numbers.pop()

    def push_data(self, num: int):
        if num == self.right_answer:
            self.reward = 1
        
        with open(self.OUTPUT_FILE, "w", newline="") as f:
            f.write("reward\\n")
            f.write(str(self.reward))
'''

class TestContainer:
	def test_build_image(self):
		client = docker.from_env()

		if len(client.images.list(filters={'reference': DOCKER_IMAGE})) > 0:
			client.images.remove(DOCKER_IMAGE, force=True)

		Container.build_image()
		client.images.get(DOCKER_IMAGE) # raises error if image doesnt exist

	def test_correct_submission(self):
		port = randrange(8000, 9000)
		with http_server(port, {
			"submission.zip": {
				"submission/build.sh": '',
				"submission/main.py": CORRECT_SUBMISSION_PY,
			},
			"validator.zip": {
				"validator/build.sh": '',
				"validator/__init__.py": '',
				"validator/validator.py": VALIDATOR_PY,
			},
			"instances/instance1.txt": '3\n1\n2\n',
		}):
			container = Container(
				submission_url=f"http://localhost:{port}/submission.zip",
				validator_url=f"http://localhost:{port}/validator.zip",
				evaluation_settings = {
					"cpu": 1,
					"memory": 512,
					"time_limit": 5,
				},
				benchmark_instances={
					"instance1": f"http://localhost:{port}/instances/instance1.txt"
				}
			)
			results = container.run()

			print(results)

			assert container.status == Status.SUCCESS
			assert int(results["instance1"]["results"][0]["reward"]) == 1

	def test_timeout_submission(self):
		port = randrange(8000, 9000)
		with http_server(port, {
			"submission.zip": {
				"submission/build.sh": '',
				"submission/main.py": TIMEOUT_SUBMISSION_PY,
			},
			"validator.zip": {
				"validator/build.sh": '',
				"validator/__init__.py": '',
				"validator/validator.py": VALIDATOR_PY,
			},
			"instances/instance1.txt": '3\n1\n2\n',
		}):
			container = Container(
				submission_url=f"http://localhost:{port}/submission.zip",
				validator_url=f"http://localhost:{port}/validator.zip",
				evaluation_settings = {
					"cpu": 1,
					"memory": 512,
					"time_limit": 5,
				},
				benchmark_instances={
					"instance1": f"http://localhost:{port}/instances/instance1.txt"
				}
			)
			results = container.run()

			print(results)

			assert container.status == Status.TIMEOUT

	def test_error_submission(self):
		port = randrange(8000, 9000)
		with http_server(port, {
			"submission.zip": {
				"submission/build.sh": '',
				"submission/main.py": ERROR_SUBMISSION_PY,
			},
			"validator.zip": {
				"validator/build.sh": '',
				"validator/__init__.py": '',
				"validator/validator.py": VALIDATOR_PY,
			},
			"instances/instance1.txt": '3\n1\n2\n',
		}):
			container = Container(
				submission_url=f"http://localhost:{port}/submission.zip",
				validator_url=f"http://localhost:{port}/validator.zip",
				evaluation_settings = {
					"cpu": 1,
					"memory": 512,
					"time_limit": 5,
				},
				benchmark_instances={
					"instance1": f"http://localhost:{port}/instances/instance1.txt"
				}
			)
			results = container.run()

			print(results)

			assert container.status == Status.ERROR

	def test_download_fail(self):
		try:
			port = randrange(8000, 9000)
			with http_server(port, {}): # no files in the server
				container = Container(
					submission_url=f"http://localhost:{port}/submission.zip",
					validator_url=f"http://localhost:{port}/validator.zip",
					evaluation_settings = {
						"cpu": 1,
						"memory": 512,
						"time_limit": 5,
					},
					benchmark_instances={
						"instance1": f"http://localhost:{port}/instances/instance1.txt"
					}
				)
				container.run()

				assert False
		except Exception:
			assert True
