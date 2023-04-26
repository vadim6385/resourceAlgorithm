"""
The class represents a task with attributes for bandwidth, start time, duration, and priority.
It includes getter and setter methods to access and modify these attributes.
"""
from enum import IntEnum
from itertools import count


class TaskPriority(IntEnum):
    REGULAR = 0
    PREMIUM = 10
    ENTERPRISE = 20


class Task:
    # create counter object for generating task id
    id_iter = count(start=1, step=1)

    # Initialize Task object with bandwidth, start_time, duration, and priority
    def __init__(self, bandwidth, start_time, duration, priority):
        self.__id = next(self.id_iter)
        self.__bandwidth = bandwidth
        self.__start_time = start_time
        self.__duration = duration
        self.__priority = priority

    # get unique task Id
    @property
    def id(self):
        return self.__id

    # Get bandwidth of the task
    @property
    def bandwidth(self):
        return self.__bandwidth

    # Get start time of the task
    @property
    def start_time(self):
        return self.__start_time

    # Set new start time for the task
    @start_time.setter
    def start_time(self, val):
        self.__start_time = val

    # Get duration of the task
    @property
    def duration(self):
        return self.__duration

    # Get priority of the task
    @property
    def priority(self):
        return self.__priority

    # Set new priority for the task
    @priority.setter
    def priority(self, val):
        self.__priority = val

    # String representation of the Task object
    def __repr__(self):
        return "Task(bandwidth={}, start_time={}, duration={}, priority={})".format(self.__bandwidth,
                                                                                    self.__start_time,
                                                                                    self.__duration,
                                                                                    self.__priority)
