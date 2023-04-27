"""
This module defines a TaskMatrix class that helps manage task and their bandwidth allocation.
"""

import numpy as np

# Constants for default end time values
DEFAULT_END_TIME = 0xFF
DEFAULT_MATRIX_END_TIME = 0x200


class TaskMatrix:
    """
    A class representing a matrix of task and their bandwidth allocation.
    """

    def __init__(self, max_bandwidth, end_time=DEFAULT_END_TIME):
        """
        Initialize the TaskMatrix.

        @param max_bandwidth: maximum bandwidth for the task matrix
        @type max_bandwidth: int
        @param end_time: end time for the task matrix, default is DEFAULT_MATRIX_END_TIME
        @type end_time: int
        """
        self.__max_bandwidth = max_bandwidth
        self.__end_time = end_time
        self.__matrix = np.zeros((self.__max_bandwidth, self.__end_time), dtype=int)
        self.__starved_tasks_list = []

    @property
    def data(self):
        """
        Get the underlying task matrix data.

        @return: the task matrix data
        @rtype: numpy.ndarray
        """
        return self.__matrix

    @property
    def starved_tasks(self):
        return self.__starved_tasks_list

    def __get_free_bandwidth_indices_list(self, time_stamp):
        """
        Get a list of indices for free bandwidth at the given time stamp.

        @param time_stamp: time stamp to check for free bandwidth
        @type time_stamp: int
        @return: count of free bandwidth and list of indices
        @rtype: tuple(int, list[int])
        """
        cnt = 0
        rows_list = []
        for i in range(self.__max_bandwidth):
            if self.__matrix[i][time_stamp] == 0:
                cnt += 1
                rows_list.append(i)
        return cnt, rows_list

    def add_task(self, task):
        """
        Add a task to the TaskMatrix and allocate bandwidth.
        @param task: task to be added
        @type task: Task
        @return: True if the task was added, False if not enough bandwidth
        @rtype: bool
        """
        bandwidth_counter = task.bandwidth
        start_time = task.actual_start_time
        free_bandwidth, free_rows_list = self.__get_free_bandwidth_indices_list(start_time)
        if bandwidth_counter > free_bandwidth:
            return False
        task_id = task.id
        task_end_time = start_time + task.duration
        # if task end time is more than allocated time, task is dropped and moved to starved task list
        if task_end_time > self.__end_time:
            self.__starved_tasks_list.append(task)
            return True
        # "paint" the appropriate places in task matrix with task id number
        for i in free_rows_list:  # matrix rows
            for j in range(start_time, task_end_time):  # matrix columns
                self.__matrix[i][j] = task_id
            bandwidth_counter -= 1
            if bandwidth_counter <= 0:
                break
        return True

    def __repr__(self):
        """
        Generate a string representation of the TaskMatrix.

        @return: string representation of the TaskMatrix
        @rtype: str
        """
        ret = "\t"
        for col in range(self.__end_time):
            ret += "{}\t".format(str(col))
        ret += "\n"
        for row in range(self.__max_bandwidth):
            ret += "{}:\t".format(str(row))
            for col in range(self.__end_time):
                ret += "{}\t".format(str(self.__matrix[row][col]))
            ret += "\n"
        return ret
