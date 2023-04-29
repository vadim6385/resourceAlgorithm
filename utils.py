from collections import deque
from enum import IntEnum
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


class TaskPriority(IntEnum):
    REGULAR = 0
    PREMIUM = 10
    ENTERPRISE = 20


class TaskStatus(IntEnum):
    PENDING = 0
    IN_PROGRESS = 1
    FINISHED = 2
    DROPPED = 3