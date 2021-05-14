import numpy as np


def pareto_optimize(list_of_dict):
    """
    Finds the pareto-optimized list of results.
    :param list_of_dict: List of dictionaries with key "Objective" as a list of costs to optimize.
    :return: List of dictionaries (list_of_dict) trimmed to only the pareto-optimized results.
    """
    costs = [engine["Objective"] for engine in list_of_dict]
    list_of_costs = np.array([np.array(point for point in costs)])
    is_efficient = is_pareto_efficient(list_of_costs)
    front = list()
    for ii in range(len(is_efficient)):
        if is_efficient[ii]:
            front.append(list_of_dict[ii])
    return front


def is_pareto_efficient(costs):
    """
    Find the pareto-efficient points.
    Adapted from https://stackoverflow.com/questions/32791911/fast-calculation-of-pareto-front-in-python.
    :param costs: An (n_points, n_costs) array
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    is_efficient = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
        is_efficient[i] = np.all(np.any(costs[:i]>c, axis=1)) and np.all(np.any(costs[i+1:]>c, axis=1))
    return is_efficient
