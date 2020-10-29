import csv


def group_dictlist_by_key(components, key):
    print(components)
    grouping = dict()
    for comp in components:
        if comp[key] in grouping:
            grouping[key] = list()
        grouping[key].append(comp[key])
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
