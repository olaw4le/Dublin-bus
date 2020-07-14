# 1. find segments in journey
# 2. query database for segment proportions
# 3. return sum of proportions

# from routeID, sub-route - return sequence of stop numbers on route
sequence = ()


def stops_on_route(route):
    """return a sequence of all stops on a given route"""
    pass


# select only stop numbers for this journey
def stops_on_journey(start, end, seq):
    """return all stops on a given route-sequence between a
        start and end start (including the start & end stop)"""

    start_index = seq.index(start)
    end_index = seq.index(end)

    return seq[start_index, end_index + 1]


def segments_on_journey(seq):
    """return list of segments on passed route-stop-sequence"""

    segments = []

    for i, stop in enumerate(seq):
        if i != 0:
            segments.append("%d-%d" % (seq[i - 1], seq[i]))

    return segments
