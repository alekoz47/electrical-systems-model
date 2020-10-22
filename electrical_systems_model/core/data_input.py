import csv

def import_epla():
    data_path = '../data/EPLA_input.csv' # come with some way to open a file explorer
    epla = []

    with open(data_path) as file:
        data = csv.DictReader(file)
        for line in data:
            epla.append(line)
    return epla

