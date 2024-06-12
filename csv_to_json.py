from csv import DictReader
from json import dumps
from os import path


def conversion():
    '''Function to convert files to json strings'''

    # convert results.scv from csv to a json string
    with open(path.join('results/results.csv')) as file:
        csv_reader = DictReader(file)
        data = list(csv_reader)
    results_string = dumps(data)

    # convert metrics.scv from csv to a json string
    with open(path.join('results/metrics.csv')) as file:
        csv_reader = DictReader(file)
        data = list(csv_reader)
    metrics_string = dumps(data)

    # convert CPU_times.scv from csv to a json string
    with open(path.join('results/CPU_times.csv')) as file:
        csv_reader = DictReader(file)
        data = list(csv_reader)
    CPU_times_string = dumps(data)

    return results_string, metrics_string, CPU_times_string

# for testing purposes only
def main():
    print(conversion())
if __name__ == '__main__':
    main()