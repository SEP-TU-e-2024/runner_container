from csv import DictReader
from json import dump
from os import path
from settings import DOCKER_RESULTS

def conversion():
    '''Function to convert files to json strings'''

    # convert results.scv from csv to a json string
    with open(path.join(DOCKER_RESULTS, 'results.csv')) as file:
        csv_reader = DictReader(file)
        data = list(csv_reader)
    results_string = dump(data)

    # convert metrics.scv from csv to a json string
    with open(path.join(DOCKER_RESULTS, 'metrics.csv')) as file:
        csv_reader = DictReader(file)
        data = list(csv_reader)
    metrics_string = dump(data)

    return results_string, metrics_string

# for testing purposes only
def main():
    print(conversion())
if __name__ == '__main__':
    main()