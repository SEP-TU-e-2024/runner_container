"""
This module contains the StartCommand class.
"""

from container import Container, Status
from custom_logger import main_logger

from .command import Command

logger = main_logger.getChild("start_command")


class StartCommand(Command):
    """
    The StartCommand class is used to start a container on the runner.
    """

    @staticmethod
    def execute(args: dict):
        container = None
        
        if any(required not in args for required in ["submission_url", "validator_url", "evaluation_settings", "benchmark_instances"]):
            return {"status": "error"}
        
        try:
            container = Container(submission_url=args["submission_url"], validator_url=args["validator_url"], benchmark_instances=args["benchmark_instances"], evaluation_settings=args["evaluation_settings"])
            results = container.run()

            status = container.status

            if status == Status.SUCCESS:
                return {"status": "ok", "results": results}
            elif status == Status.TIMEOUT:
                return {"status": "error", "cause": "timeout"}
            else:
                return {"status": "error", "cause": "error"}
        except Exception:
            logger.error(f"Container running produced error for args {args}", exc_info=1)
            return {"status": "error", "cause": "internal_error"}
        finally:
            if container is not None:
                container.tidy()