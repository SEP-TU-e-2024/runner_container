import os

import psutil

import subprocess

import re

class IOModule:
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
        return {'score':0}
    
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

    def __extract_VmPeak(info_string):
        """
        Function to extract the VmPeak value from the process status output.
        """
        pattern = r'VmPeak:\s*([0-9]+)\s+kB'
        match = re.search(pattern, info_string)

        if match:
            return match.group(1)
        else:
            return None

    def __del__(self):
        """On termination of the program (when this object will be deleted) this will write all performance and score metrics to a file"""

        # get cpu times
        current_process = psutil.Process(os.getpid())
        cpu_times = current_process.cpu_times();
        cpu_times_sum = cpu_times.user + cpu_times.system + cpu_times.children_user + cpu_times.children_system;

        # obtain MaxRSS from /proc/{pid}/status
        proc_directory = '/proc/' + str(os.getpid()) + '/status'
        result = subprocess.run(['cat', proc_directory], capture_output=True, text=True)
        
        max_memory = self.__extract_VmPeak(result.stdout)

        # Write metrics to csv file
        metrics_file = open(self._OUTPUT_FILE, 'w', newline='')
        metrics_file.write("Max RAM usage (kB), CPU Time (s), Score\n")
        metrics_file.write(max_memory + ", ")
        metrics_file.write(str(cpu_times_sum) + ", ")
        metrics_file.write(str(self._score()['score']))
        metrics_file.close()