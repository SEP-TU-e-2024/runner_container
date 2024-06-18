class IOModule:  # noqa: N999
    """
    This is a base class that should be used as a template for the Validator.
    It defines some basic functionality that should be implemented by the Validator: _score, obtain_data and push_data.
    Additionally it will push all performance metrics and scoring data to a file on termination of the program.
    """

    _OUTPUT_FILE = "/results/results.csv"
    _PERFORMANCE_ATTRS = ["cpu_times", "memory_full_info"]

    def _score(self) -> dict:
        """
        _score defines all problem specific metrics and computes those values, it must be overwritten by Validator.
        It must return a dictionary where it maps each metric to a value (dict[string, any type]).
        """
        return {"score": 0}

    def obtain_data(self):
        """
        obtain_data is called by the submission code to obtain a new (or the initial) state of the current problem.
        The Validator must overwrite this function and define the appropriate return datatype.
        """
        pass

    def push_data(self):
        """
        push_data is called by the submission code to push a new solution it has computed to the validator.
        The Validator must overwrite this function and define the appropriate datatype for such a solution.
        """
        pass

    def __del__(self):
        """On termination of the program (when this object will be deleted) this will write all performance and score metrics to a file"""

        # Write score metrics to csv file
        metrics_file = open(self._OUTPUT_FILE, "w", newline="")
        scores = self._score()
        metrics_file.write(','.join(scores.keys()) + '\n')
        metrics_file.write(','.join([str(x) for x in scores.values()]) + '\n')
        metrics_file.close()
