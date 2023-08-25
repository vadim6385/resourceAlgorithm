from _operator import attrgetter
from collections import deque


def sort_queue(Q, attrib, reverse=False):
    """
    sort deque by attribute
    :param Q: deque to sort
    :param attrib: deque sort by attribute
    :return: sorted deque
    """
    return deque(sorted(Q, key=attrgetter(attrib), reverse=reverse))
