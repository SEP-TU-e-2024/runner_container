#----------------------------------------------------------------
# Docker
#----------------------------------------------------------------
DOCKER_FILE_PARRENT_DIR = "." # just for testing
#DOCKER_IMAGE = "runnercontainer"

# Mounts
DOCKER_SUBMISSION = "/submission"
DOCKER_VALIDATOR = "/validator"
DOCKER_RESULTS = "/results"

# Time, Memory and CPU
DOCKER_TIMEOUT = 10
DOCKER_MEMORY = "512m"
DOCKER_CPUS = 2