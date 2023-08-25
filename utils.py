from collections import deque
from operator import attrgetter


def DEBUG_HALT():
    assert 0 == 1, "DEBUG_HALT"


def ASSERT(stmt):
    assert stmt, "ASSERT"


def sort_queue(Q, attrib, reverse=False):
    """
    sort deque by attribute
    :param Q: deque to sort
    :param attrib: deque sort by attribute
    :return: sorted deque
    """
    return deque(sorted(Q, key=attrgetter(attrib), reverse=reverse))


