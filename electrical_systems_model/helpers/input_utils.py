import csv


def group_dictlist_by_key(components, key):
    grouping = dict()
    for comp in components:
        if comp[key] not in grouping:
            grouping[comp[key]] = list()
        grouping[comp[key]].append(comp)
    return grouping


def import_csv_as_dictlist(data_path):
    # TODO: decide on file explorer or specific folder into which user places epla
    # TODO: document proper format of epla
    dictlist = list()

    with open(data_path) as file:
        data = csv.DictReader(file)
        for line in data:
            dictlist.append(line)
    return dictlist
