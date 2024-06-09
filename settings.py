# ----------------------------------------------------------------
# Connection
# ----------------------------------------------------------------

JUDGE_HOST = "localhost"
"""
Host of the the judge server.
"""

JUDGE_PORT = 12345
"""
The port of the judge server.
"""

RETRY_WAIT = 5
"""
Time in seconds to wait before retrying to connect to the judge server.
"""

# ----------------------------------------------------------------
# Docker
# ----------------------------------------------------------------
DOCKER_IMAGE = "test"

# Mounts
DOCKER_SUBMISSION = "/submission"
DOCKER_VALIDATOR = "/validator"
DOCKER_RESULTS = "/results"
