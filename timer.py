import psutil
import sys
import time
import subprocess
import re
import os

def time_file_exists():
    if os.path.exists("time.txt"):
        return os.stat("time.txt").st_size != 0
    return False

#import gputil
def main():
    # Check if the correct number of arguments are provided
    if os.path.exists("/usr/bin/time") == False:
        print("time is not installed")
        return

    if len(sys.argv) < 3:
        print("Usage: python3 timer.py time_limit executable <arguments of executable>")
        return

    time_limit = float(sys.argv[1]) # time limit in seconda
    executable_path = sys.argv[2] # path to the executable
    executable_args = " ".join(sys.argv[3:]) # arguments of the executable

    # use the GNU time command for time tracking reasons
    evaluated_executable = "time -o time.txt " + executable_path + " " + executable_args

    if os.path.exists("time.txt"):
        os.remove("time.txt")

    # start timer for the time limit
    start_time = time.time()

    # run the executable and obtain its pid
    evaluated_process = subprocess.Popen(evaluated_executable, shell=True)
    evaluated_pid = evaluated_process.pid
    psutil_process = psutil.Process(evaluated_pid)

    # check every second if the time limit is still valid and if the process is still running
    while(time_file_exists() == False): #psutil_process.is_running()):
        if(time.time() - start_time > time_limit):
            print("time limit exceded")
            break
            #return
        else:
            print("cpu time: ", psutil_process.cpu_times().user + psutil_process.cpu_times().system)
            # add monitoring of the metrics here
            time.sleep(1)

    # write the results to a csv file
    csv_output = open("output.csv", "w")
    if not time_file_exists():
        print("submission not valid")
        csv_output.write("not_valid\n")
    else:
        times_file = open("time.txt", "r")
        lines = times_file.readlines()
        user_time = 0.0
        system_time = 0.0
        wall_time = "0:0.00"
        cpu_time = 0.0
        try:
            user_time = float(re.findall('[\d.]+',(lines[0].split()[0]))[0]) # time in user mode
            system_time = float(re.findall('[\d.]+',(lines[0].split()[1]))[0]) # time in syscalls
            wall_time = (re.findall('[\d.:]+',(lines[0].split()[2]))[0]) # wall time
            cpu_time = user_time + system_time # total cpu time
        except:
            print("error reading time file, tested executable might have crashed")

        print("wall_time: ", wall_time, " cpu_time: ", cpu_time)
        csv_output.write("command,user_time,system_time,cpu_time,wall_time\n")
        csv_output.write(executable_path + "," + str(user_time) + "," + str(system_time) + ","
                        + str(cpu_time) + "," + wall_time + "\n")

    if os.path.exists("time.txt"):
        os.remove("time.txt")

if __name__ == "__main__":
    main()