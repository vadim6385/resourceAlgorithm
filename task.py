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

    # Initialize Task object with bandwidth, created_time, duration, and priority
    def __init__(self, bandwidth, created_time, duration, priority):
        self.__id = next(self.id_iter)
        self.__bandwidth = bandwidth
        self.__created_time = created_time
        self.__actual_start_time = created_time
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

    # Get created time of the task
    @property
    def created_time(self):
        return self.__created_time

    @property
    def actual_start_time(self):
        return self.__actual_start_time

    @actual_start_time.setter
    def actual_start_time(self, val):
        self.__actual_start_time = val

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

    @property
    def actual_end_time(self):
        return self.__actual_start_time + self.__duration

    # String representation of the Task object
    def __repr__(self):
        return "Task(id={} bandwidth={}, created_time={}, actual start time{}, duration={}, actual end time={}, priority={})".format(
            self.__bandwidth,
            self.__id,
            self.__created_time,
            self.__actual_start_time,
            self.__duration,
            self.actual_end_time,
            self.__priority)
