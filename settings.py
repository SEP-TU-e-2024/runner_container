"""
This module contains the settings for the runner.
"""

import os

import dotenv

dotenv.load_dotenv()

# ----------------------------------------------------------------
# Connection
# ----------------------------------------------------------------

JUDGE_HOST = os.getenv("JUDGE_HOST", "localhost") # TODO: change to prod version, currently IP of the jumpbox, ask Teun for how to use it
"""
Host of the the judge server.
"""

JUDGE_PORT = int(os.getenv("JUDGE_PORT", "12345"))
"""
The port of the judge server.
"""

RETRY_WAIT = int(os.getenv("JUDGE_CONNECTION_RETRY_WAIT", "5"))
"""
Time in seconds to wait before retrying to connect to the judge server.
"""

# ----------------------------------------------------------------
# Docker
# ----------------------------------------------------------------
DOCKER_IMAGE = "runnercontainer"

# Mounts
DOCKER_BASE = "/app"
DOCKER_SUBMISSION = "/submission"
DOCKER_VALIDATOR = "/validator"
DOCKER_INSTANCES = "/instances"
DOCKER_RESULTS = "/results"


# ----------------------------------------------------------------
# Container settings
# ----------------------------------------------------------------
REQUIRED_SETTINGS = ["cpu", "memory", "time_limit"]