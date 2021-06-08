def estimate_cable_length(loc1, loc2):
    """
    Estimates cable length between two locations on the vessel. Assumes cables run to centerline first.
    :param loc1: list of length 3
    :param loc2: list of length 3
    :return: distance
    """
    
    # This finds the longitudinal distance in meters between the parent and child of the cable
    long_distance = loc2[0] - loc1[0]

    # This find the transverse length of cable in meters assuming the
    # cable will run from the child and parent all the way to centerline before running longitudinally
    tran_distance = abs(loc2[1]) + abs(loc1[1])

    # This finds the longitudinal distance in meters between the parent and child of the cable
    vert_distance = loc2[2] - loc1[2]

    return abs(long_distance) + abs(tran_distance) + abs(vert_distance)
